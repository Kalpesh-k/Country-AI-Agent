from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from graph import build_graph
from utils.logger import get_logger


logger = get_logger()
graph = build_graph()

app = FastAPI(title="Country Info AI Agent - Production")

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/ask")
def ask(query: str = Query(...)):
    logger.info(f"Received query: {query}")
    try:
      
        initial_state = {"query": query}
        result = graph.invoke(initial_state)
        answer = result.get("answer", "I'm sorry, I couldn't generate an answer.")
        
        logger.info(f"Successfully processed query via Multi-Node Graph. Result summary: {str(answer)[:50]}...")
        return {"response": answer}
        
    except Exception as e:
        logger.error(f"Error in Multi-Node workflow for query '{query}': {e}", exc_info=True)
        return {"response": "I'm sorry, I encountered an internal error. Please try again later."}
