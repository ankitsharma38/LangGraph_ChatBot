from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", streaming=True)

# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

def chatbot(state):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
