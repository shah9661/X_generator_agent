from typing import Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from pydantic import BaseModel,Field

load_dotenv()

generator_llm = ChatOpenAI(model="gpt-4.1",api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com", temperature=0.9)
evaluator_llm = ChatOpenAI(model="gpt-4.1",api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com", temperature=0.2)
optimizer_llm = ChatOpenAI(model="gpt-4.1",api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com", temperature=0.8)

    
class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(
        ..., description="Final evaluation result."
    )
    feedback: str = Field(..., description="Constructive feedback for the tweet.")


structured_evaluator_llm = evaluator_llm.with_structured_output(TweetEvaluation)