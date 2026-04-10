import os
from typing import TypedDict, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from utils.tools import search_country_data
from utils.logger import get_logger

load_dotenv(override=True)
logger = get_logger()


class GraphState(TypedDict):
    """
    Explicit state for our multi-node graph.
    """
    query: str
    country: Optional[str]
    fields: List[str]
    raw_data: Optional[str]
    answer: Optional[str]
    error: Optional[str]


class IntentOutput(BaseModel):
    country: Optional[str] = Field(description="The standard name of the country identified in the query.")
    fields: List[str] = Field(description="The specific attributes requested (e.g., population, capital, currency).")
    is_country_query: bool = Field(description="Whether the query is actually about a country.")


api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key


llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0)

def intent_node(state: GraphState):
    """
    STEP 1: Intent / Field Identification
    Identifies the country and requested fields from the user query.
    """
    logger.info(f"Node: Intent Identification for query: {state['query']}")
    
    prompt = f"""Analyze the following user query and extract country information.
    Query: {state['query']}
    
    If it's not about a country (e.g., coding, math, general chat), set 'is_country_query' to False.
    Always standardise country names (e.g., 'USA' -> 'United States')."""
    
    try:
        structured_llm = llm.with_structured_output(IntentOutput)
        extraction = structured_llm.invoke(prompt)
        
        if not extraction.is_country_query:
            return {
                "answer": "I am specialized only in country-related intelligence. How can I help you with country data today?",
                "error": "off_topic"
            }
        
        return {
            "country": extraction.country,
            "fields": extraction.fields,
            "error": None
        }
    except Exception as e:
        logger.error(f"Intent Error: {e}")
        return {"error": str(e)}

def tool_node(state: GraphState):
    """
    STEP 2: Tool Invocation
    Fetches raw data from the API based on the identified country.
    """
    if state.get("error") or not state.get("country"):
        return state

    logger.info(f"Node: Tool Invocation for country: {state['country']}")
    
  
    try:
        result = search_country_data.invoke({"country_name": state["country"]})
        return {"raw_data": str(result)}
    except Exception as e:
        logger.error(f"Tool Node Error: {e}")
        return {"error": f"API Error: {e}"}

def answer_node(state: GraphState):
    """
    STEP 3: Answer Synthesis
    Synthesizes the final answer using the raw data and user query.
    """
    if state.get("error") == "off_topic":
        return state
    
    if state.get("error"):
         return {"answer": f"I encountered an issue while gathering data: {state['error']}"}

    if not state.get("raw_data") or "No data found" in state.get("raw_data", ""):
        return {"answer": f"I'm sorry, I couldn't find any official data for '{state.get('country')}'. Please verify the spelling."}

    logger.info("Node: Answer Synthesis")
    
    prompt = f"""You are a professional Country Intelligence Agent.
    User Query: {state['query']}
    Retrieved Data: {state['raw_data']}
    
    Based ONLY on the retrieved data, provide a concise and friendly answer to the user's specific question. 
    Use Markdown for formatting. Do not mention internal technical terms like 'node' or 'tool'."""
    
    response = llm.invoke(prompt)
    
  
    raw_content = response.content
    if isinstance(raw_content, list):
        answer = "".join([part.get("text", "") for part in raw_content if isinstance(part, dict)])
    else:
        answer = raw_content
        
    return {"answer": answer}


workflow = StateGraph(GraphState)

workflow.add_node("intent", intent_node)
workflow.add_node("tool", tool_node)
workflow.add_node("answer", answer_node)

workflow.add_edge(START, "intent")
workflow.add_edge("intent", "tool")
workflow.add_edge("tool", "answer")
workflow.add_edge("answer", END)

graph = workflow.compile()

def build_graph():
    """
    Returns the compiled multi-node StateGraph.
    """
    logger.info("Multi-node StateGraph successfully built.")
    return graph
