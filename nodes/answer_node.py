from langchain_google_genai import ChatGoogleGenerativeAI
from utils.logger import get_logger

logger = get_logger()

def get_answer_node(llm: ChatGoogleGenerativeAI):
    def answer_node(state):
        if state.get("error") == "off_topic":
            return state
        
        if state.get("error"):
             if state["error"] == "capacity_reached":
                 return {"answer": "The intelligence service is currently experiencing high demand. I am re-establishing the secure link—please try your request again in a few seconds."}
             return {"answer": f"The intelligence scan encountered an issue: {state['error']}"}

        if not state.get("raw_data") or "No data found" in state.get("raw_data", ""):
            return {"answer": f"I couldn't find official intelligence for '{state.get('country')}'. Please check the name and try again."}

        logger.info("Node: Answer Synthesis")
        
        prompt = f"""You are the Country Intelligence Agent.
        User Query: {state['query']}
        Intelligence Data: {state['raw_data']}
        
        STRICT GUIDELINE: 
        Only answer the SPECIFIC question asked in the 'User Query'. 
        Do not include extraneous information unless requested.
        
        FORMATTING:
        - Use simple sentences for single facts.
        - Use a small Intelligence Card (### Header and - **Key**: Value) for multiple facts.
        - Maintain a professional tone."""
        
        try:
            response = llm.invoke(prompt)
            
            raw_content = response.content
            if isinstance(raw_content, list):
                answer = "".join([part.get("text", "") for part in raw_content if isinstance(part, dict)])
            else:
                answer = raw_content
                
            return {"answer": answer}
        except Exception as e:
            error_str = str(e)
            logger.error(f"Answer Error: {error_str}")
            status_keywords = ["503", "429", "demand", "deadline", "quota", "exhausted", "resource", "limit"]
            if any(x in error_str.lower() for x in status_keywords):
                return {"answer": "The intelligence service is currently experiencing high demand. I am re-establishing the secure link—please try your request again in a few seconds."}
            return {"answer": "The intelligence scan encountered an unexpected issue."}
        
    return answer_node
