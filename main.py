from dotenv import load_dotenv
load_dotenv()

from graph import build_graph
from langchain_core.messages import HumanMessage, AIMessage
from nodes.bot import llm
import re
import sys
import time

app = build_graph()

print("LangGraph Chatbot Started 🚀")
print("Type 'exit' to quit\n")

messages = []

def clean_markdown(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    return text

while True:
    user = input("You: ")
    if user.lower() in ["exit", "quit", "bye"]:
        break

    messages.append(HumanMessage(content=user))
    
    try:
        print("AI: ", end="", flush=True)
        
        full_response = ""
        for chunk in llm.stream(messages):
            if chunk.content:
                # Print character by character for typing effect
                for char in chunk.content:
                    print(char, end="", flush=True)
                    time.sleep(0.01)  # Small delay for typing effect
                full_response += chunk.content
        
        print()  # New line
        
        messages.append(AIMessage(content=full_response))
        
    except Exception as e:
        error = str(e)
        if '429' in error:
            print("\n API quota exceeded. Wait 24 hours or use new API key")
        else:
            print(f"\n Error: {error[:100]}")
        messages.pop()
