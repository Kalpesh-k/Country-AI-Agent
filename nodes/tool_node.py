from utils.tools import search_country_data
from utils.logger import get_logger

logger = get_logger()

def get_tool_node():
    def tool_node(state):
        if state.get("error") or not state.get("country"):
            return state

        logger.info(f"Node: Tool Invocation for country: {state['country']}")
        
        try:
            result = search_country_data.invoke({"country_name": state["country"]})
            return {"raw_data": str(result)}
        except Exception as e:
            logger.error(f"Tool Error: {e}")
            return {"error": f"Search failed: {e}"}
            
    return tool_node
