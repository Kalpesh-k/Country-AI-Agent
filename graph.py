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
    query: str
    country: Optional[str]
    fields: List[str]
    raw_data: Optional[str]
    answer: Optional[str]
    error: Optional[str]

class IntentOutput(BaseModel):
    country: Optional[str] = Field(description="Standard country name.")
    fields: List[str] = Field(description="Requested attributes.")
    is_country_query: bool = Field(description="Whether query is about a country.")

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0)

def intent_node(state: GraphState):
    logger.info(f"Node: Intent for {state['query']}")
    
    prompt = f"""Identify the country and data requirements from this query:
    Query: {state['query']}
    
    Note: If it isn't about country facts, mark is_country_query as False.
    Standardize all country names."""
    
    try:
        structured_llm = llm.with_structured_output(IntentOutput)
        extraction = structured_llm.invoke(prompt)
        
        if not extraction.is_country_query:
            return {
                "answer": "This agent specializes in global country intelligence. Please provide a country name to start an analytical search.",
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
    if state.get("error") or not state.get("country"):
        return state

    logger.info(f"Node: Researching {state['country']}")
    
    try:
        result = search_country_data.invoke({"country_name": state["country"]})
        return {"raw_data": str(result)}
    except Exception as e:
        logger.error(f"Tool Error: {e}")
        return {"error": f"Search failed: {e}"}

def answer_node(state: GraphState):
    if state.get("error") == "off_topic":
        return state
    
    if state.get("error"):
         return {"answer": f"The intelligence scan encountered an issue: {state['error']}"}

    if not state.get("raw_data") or "No data found" in state.get("raw_data", ""):
        return {"answer": f"I couldn't find official intelligence for '{state.get('country')}'. Please check the name and try again."}

    logger.info("Node: Final Synthesis")
    
    prompt = f"""You are the Country Intelligence Agent.
    User Query: {state['query']}
    Intelligence Data: {state['raw_data']}
    
    STRICT GUIDELINE: 
    Only answer the SPECIFIC question asked in the 'User Query'. 
    Do not include extraneous information (like population or capital) unless the user specifically asked for it.
    
    FORMATTING:
    - If the user asked for one specific fact, provide it in a simple sentence.
    - If multiple facts were requested, use a small Intelligence Card (### Header and - **Key**: Value).
    - Maintain a professional and helpful tone."""
    
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
    logger.info("Intelligence Graph Built.")
    return graph
