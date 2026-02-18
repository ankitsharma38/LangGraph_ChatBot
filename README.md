# LangGraph Chatbot Backend

A conversational AI chatbot built with LangGraph, FastAPI, and Google Gemini/OpenAI.

## What is LangGraph?

LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain to enable:
- **State Management**: Maintain conversation context across multiple turns
- **Graph-based Workflows**: Define complex conversation flows as graphs
- **Streaming Support**: Real-time response streaming
- **Thread Management**: Handle multiple conversation sessions

## Features

- ✅ Real-time streaming responses
- ✅ Thread-based conversation management
- ✅ Support for Google Gemini & OpenAI models
- ✅ RESTful API with FastAPI
- ✅ CORS enabled for frontend integration

## Prerequisites

- Python 3.10+
- Google Gemini API Key or OpenAI API Key

## Installation

### 1. Clone the repository
```bash
cd langgraph-chatbot
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup environment variables

Create a `.env` file:
```bash
# For Google Gemini
GOOGLE_API_KEY=your_google_api_key_here

# For OpenAI (optional)
# OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key:
- Google Gemini: https://aistudio.google.com/api-keys
- OpenAI: https://platform.openai.com/api-keys

## Usage

### Run the API server
```bash
python api.py
```

Server will start at: `http://localhost:8000`

### Run CLI chatbot (optional)
```bash
python main.py
```

## API Endpoints

### POST `/api/chat/stream`
Stream chat responses with typing effect

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "thread_id": "optional-thread-id"
}
```

**Response:** Server-Sent Events (SSE)
```
data: {"thread_id": "uuid"}
data: {"content": "H"}
data: {"content": "i"}
...
```

### GET `/api/threads/{thread_id}`
Get conversation history for a thread

## Project Structure

```
langgraph-chatbot/
├── nodes/
│   └── bot.py          # LLM configuration
├── api.py              # FastAPI server
├── graph.py            # LangGraph workflow
├── state.py            # State definition
├── main.py             # CLI interface
├── config.py           # Configuration
├── .env                # Environment variables
└── requirements.txt    # Dependencies
```

## Switch Between Models

Edit `nodes/bot.py`:

**Google Gemini:**
```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", streaming=True)
```

**OpenAI:**
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
```

## Troubleshooting

**API Key not loading:**
- Ensure `.env` file is in the project root
- Add `load_dotenv()` at the top of your files

**Module not found:**
```bash
pip install -r requirements.txt
```

**Port already in use:**
```bash
# Change port in api.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## License

MIT
