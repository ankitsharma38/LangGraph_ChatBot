from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def chatbot(state):
    response = llm.invoke(state["message"])
    return {"message": response.content}
