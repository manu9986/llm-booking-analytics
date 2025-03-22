from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.analytics import router as analytics_router  # Import the analytics router
from app.rag import query_rag  # Import the query_rag function from rag.py
import time
import logging
from fastapi import Request


# Initialize FastAPI app
app = FastAPI()

# Define request and response models for /ask endpoint
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM-Powered Booking Analytics & QA System"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(query_request: QueryRequest):
    try:
        answer = query_rag(query_request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")

# Include the analytics router
app.include_router(analytics_router, prefix="/api")

logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logging.info(f"Request {request.method} {request.url.path} took {duration:.4f} seconds")
    return response


# Run the FastAPI app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
