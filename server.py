from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
 
from database import init_db, save_tweet, get_history
from graph import workflow

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Database initialized")

    yield
 
 
app = FastAPI(
    title="Tweet Generator API",
    description="AI-powered tweet generator using LangGraph",
    version="1.0.0",
    lifespan=lifespan,
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
 
class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200, example="Monday mornings")
    max_iteration: int = Field(default=3, ge=1, le=10)
 
 
class GenerateResponse(BaseModel):
    topic: str
    final_tweet: str
    status: str                  
    iterations_used: int
    max_iteration: int
    tweet_history: list[str]
    feedback_history: list[str]
 
class HistoryItem(BaseModel):
    id: int
    topic: str
    final_tweet: str
    status: str
    iterations_used: int
    created_at: str


 
@app.get("/health")
def health():
    """Quick check — is the server alive?"""
    return {"status": "ok", "service": "tweet-generator"}
 
 
@app.post("/generate-tweet", response_model=GenerateResponse)
def generate_tweet(req: GenerateRequest):
    """
    Run the full generate → evaluate → optimize pipeline.
    Returns the best tweet found within max_iteration loops.
    """
    try:
        result = workflow.invoke({
            "topic": req.topic,
            "iteration": 0,
            "max_iteration": req.max_iteration,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
    response_data = {
        "topic":            result["topic"],
        "final_tweet":      result["tweet"],
        "status":           result["evaluation"],
        "iterations_used":  result["iteration"],
        "max_iteration":    result["max_iteration"],
        "tweet_history":    result.get("tweet_history", []),
        "feedback_history": result.get("feedback_history", []),
    }
    try:
        new_id = save_tweet(response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB save error: {str(e)}")
 
    return GenerateResponse(id=new_id, **response_data)

@app.get("/history", response_model=list[HistoryItem])
def history(limit: int = Query(default=20, ge=1, le=100)):
    """
    Fetch past generated tweets from PostgreSQL, newest first.
    Optional ?limit=N query param (default 20, max 100).
    """
    try:
        rows = get_history(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")
 
    return [
        HistoryItem(
            id=row["id"],
            topic=row["topic"],
            final_tweet=row["final_tweet"],
            status=row["status"],
            iterations_used=row["iterations_used"],
            created_at=str(row["created_at"]),)
        for row in rows
    ]
