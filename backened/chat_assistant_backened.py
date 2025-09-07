import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from  backened.utils.model import EuriLLM
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage,AIMessage,HumanMessage

#model
model=EuriLLM()

#create the state of application
class ChatState(TypedDict):
    message:Annotated[list[BaseMessage],add_messages]

#define graph state
graph=StateGraph(ChatState)


#define task
def chat(state:ChatState):
    msg=state['message']
    response=model.invoke(msg)
    return {'message':[AIMessage(content=response)]}

#create node
graph.add_node('chat',chat)

#connect edge between nodes
graph.add_edge(START,'chat')
graph.add_edge('chat',END)

#compile graph
checkpointer=InMemorySaver()
workflow=graph.compile(checkpointer=checkpointer)













