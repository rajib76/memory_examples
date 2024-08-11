# In this example, I explored some of the features of mem0
import operator
import os
from typing import TypedDict, Annotated, Sequence

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from mem0 import MemoryClient
from openai import OpenAI

openai_client = OpenAI()

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MEM0_API_KEY = os.environ.get('MEM0_API_KEY')
client = MemoryClient(api_key=MEM0_API_KEY)

user = "mohan"

llm = ChatOpenAI()


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


def agent_with_memory(state):
    print("state ", state)
    query = state["messages"][-1]
    print("query ", query)
    memory = client.search(query, user_id=user)

    system_prompt = """You're a helpful travel agent. You provide vacation travel 
    consulting service to your customers. You must be inquisitive and be like a 
    friend to your customers. Get to know your customers well, so that you can 
    provide more personalized experience to them,To make the 
    conversation personal, please also leverage the information you already know about them.
    """

    system_message = {
        "role": "system", "content": system_prompt
    }

    formatted_message = f"""
        \n Below are memories from past interactions:
        {memory}
        End of memories.
        """

    user_message = {
        "role": "user", "content": query + formatted_message
    }

    messages = [
        system_message,
        user_message
    ]

    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    response = completion.choices[0].message.content
    print("response ", response)

    client.add([
        {"role": "user", "content": query},
        {"role": "assistant", "content": response}
    ], user_id=user)
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("agent_with_memory", agent_with_memory)
graph_builder.set_entry_point("agent_with_memory")
graph_builder.set_finish_point("agent_with_memory")
graph = graph_builder.compile()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [user_input]}):
        for key, value in event.items():
            print("key ", key)
            print("value ", value)
