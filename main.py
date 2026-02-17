from dotenv import load_dotenv
load_dotenv()

from graph import build_graph

app = build_graph()

print("LangGraph Chatbot Started 🚀")

while True:
    user = input("You: ")
    if user.lower() == "exit":
        break

    result = app.invoke({"message": user})
    print("Bot:", result["message"])
