from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from nodes.bot import llm
import json
import uuid
from typing import Optional

load_dotenv()

app = FastAPI()

# In-memory storage for threads
threads = {}

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
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    thread_id: str

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    # Get or create thread ID
    thread_id = request.thread_id or str(uuid.uuid4())
    
    # Get thread history or create new
    if thread_id not in threads:
        threads[thread_id] = []
    
    # Convert frontend messages to LangChain format
    lc_messages = []
    for msg in request.messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    
    # Store in thread
    threads[thread_id] = lc_messages
    
    async def generate():
        # Send thread_id first
        yield f"data: {json.dumps({'thread_id': thread_id})}\n\n"
        
        full_response = ""
        for chunk in llm.stream(lc_messages):
            if chunk.content:
                full_response += chunk.content
                yield f"data: {json.dumps({'content': chunk.content})}\n\n"
        
        # Store bot response in thread
        threads[thread_id].append(AIMessage(content=full_response))
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/api/threads/{thread_id}")
async def get_thread(thread_id: str):
    if thread_id not in threads:
        return {"messages": []}
    
    # Convert to frontend format
    messages = []
    for msg in threads[thread_id]:
        if isinstance(msg, HumanMessage):
            messages.append({"role": "user", "content": msg.content})
        else:
            messages.append({"role": "assistant", "content": msg.content})
    
    return {"messages": messages}

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
