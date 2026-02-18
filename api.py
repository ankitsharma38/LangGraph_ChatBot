from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from nodes.bot import llm
import json

load_dotenv()

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build LangGraph
# chatbot = build_graph()

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    # Convert frontend messages to LangChain format
    lc_messages = []
    for msg in request.messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    
    async def generate():
        for chunk in llm.stream(lc_messages):
            if chunk.content:
                yield f"data: {json.dumps({'content': chunk.content})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Convert frontend messages to LangChain format
    lc_messages = []
    for msg in request.messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    
    # Invoke LLM directly
    full_response = ""
    for chunk in llm.stream(lc_messages):
        full_response += chunk.content
    
    # Return bot response
    return ChatResponse(response=full_response)

@app.get("/")
async def root():
    return {"message": "LangGraph Chatbot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
