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
def ask(query: str = Query(...)):
    logger.info(f"Query: {query}")
    try:
        result = graph.invoke({"query": query})
        answer = result.get("answer", "No intelligence synthesized.")
        logger.info(f"Service completed analytical scan.")
        return {"response": answer}
    except Exception as e:
        logger.error(f"Service Error: {e}")
        return {"response": "The intelligence node encountered a temporary failure."}
