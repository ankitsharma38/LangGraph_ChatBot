from langgraph.graph import StateGraph, START, END
from state import ChatState
from nodes.bot import chatbot

def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("bot", chatbot)

    graph.add_edge(START, "bot")
    graph.add_edge("bot", END)

    return graph.compile()
