from dotenv import load_dotenv
load_dotenv()

from graph import build_graph
from langchain_core.messages import HumanMessage
import re

app = build_graph()

print("LangGraph Chatbot Started 🚀")
print("Type 'exit' to quit\n")

messages = []

def clean_markdown(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    return text

while True:
    user = input("User: ")
    if user.lower() in ["exit", "quit"]:
        break

    messages.append(HumanMessage(content=user))
    result = app.invoke({"messages": messages})
    messages = result["messages"]
    
    print("AI:", clean_markdown(messages[-1].content))
