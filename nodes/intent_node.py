from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.logger import get_logger

logger = get_logger()

class IntentOutput(BaseModel):
    country: Optional[str] = Field(description="Standard country name.")
    fields: List[str] = Field(description="Requested attributes.")
    is_country_query: bool = Field(description="Whether query is about a country.")

def get_intent_node(llm: ChatGoogleGenerativeAI):
    def intent_node(state):
        logger.info(f"Node: Intent Identification for query: {state['query']}")
        
        prompt = f"""Identify the country and data requirements from this query:
        Query: {state['query']}
        Previous Context (Country): {state.get('context') or 'None'}
        
        If the query is a follow-up (e.g., 'currency?', 'population?'), use the 'Previous Context' country.
        If it isn't about country facts, mark is_country_query as False.
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
            
    return intent_node
