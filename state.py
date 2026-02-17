from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


#BaseMessage list[BaseMessage] - Python list mein messages store hote hain
#add_messages - ek function hai jo messages ko graph ke state mein add karta hai, taki chatbot unhe process kar sake.
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
