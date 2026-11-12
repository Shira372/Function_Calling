# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from agent_service import agent

app = FastAPI()

class QueryRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    response = agent(request.message)
    return {"response": response}
