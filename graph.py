import os
from typing import TypedDict, List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

from nodes.intent_node import get_intent_node
from nodes.tool_node import get_tool_node
from nodes.answer_node import get_answer_node
from utils.logger import get_logger

load_dotenv(override=True)
logger = get_logger()

class GraphState(TypedDict):
    query: str
    context: Optional[str]
    country: Optional[str]
    fields: List[str]
    raw_data: Optional[str]
    answer: Optional[str]
    error: Optional[str]

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0, max_retries=3)


def build_graph():
    workflow = StateGraph(GraphState)

    
    intent_node = get_intent_node(llm)
    tool_node = get_tool_node()
    answer_node = get_answer_node(llm)

   
    workflow.add_node("intent", intent_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("answer", answer_node)

  
    workflow.add_edge(START, "intent")
    workflow.add_edge("intent", "tool")
    workflow.add_edge("tool", "answer")
    workflow.add_edge("answer", END)

    logger.info("Modular 3-Node StateGraph successfully built.")
    return workflow.compile()
