from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from graph import build_graph
from utils.logger import get_logger

logger = get_logger()
graph = build_graph()

app = FastAPI(title="Country Intelligence Service")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/ask")
def ask(query: str = Query(...), context: str = Query(None)):
    logger.info(f"Query: {query} | Context: {context}")
    try:
        initial_state = {"query": query, "context": context}
        result = graph.invoke(initial_state)
        
        answer = result.get("answer", "No intelligence synthesized.")
        country = result.get("country")
        
        logger.info(f"Service completed analytical scan.")
        return {
            "response": answer,
            "country": country
        }
    except Exception as e:
        logger.error(f"Service Error: {e}")
        return {"response": "The Intelligence Bot encountered a temporary failure. Please try again later."}
