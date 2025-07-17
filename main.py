import os
import json
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_tavily import TavilySearch


# Load environment variables from .env file
load_dotenv()

# Load configuration from config.json
with open('config.json', 'r') as f:
    config_data = json.load(f)

# Set the API keys from environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

tool = TavilySearch(max_results=config_data['tools']['tavily_search']['max_results'])
tools = [tool]


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]


# Define the agent node
def call_model(state: AgentState, config):
    messages = state["messages"]
    
    # Add a system prompt to encourage tool use
    system_prompt = config_data['prompts']['system_prompt']
    
    # Prepend the system prompt to the messages, but only if it's the first message
    if len(messages) == 1:
        messages = [
            HumanMessage(content=system_prompt),
            messages[0]
        ]

    model = ChatGoogleGenerativeAI(
        temperature=config_data['model']['temperature'], model=config_data['model']['name']
    )
    model = model.bind_tools(tools)
    response = model.invoke(messages, config)
    return {"messages": [response]}


# Define the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    tools_condition,
)
workflow.add_edge("tools", "agent")

app = workflow.compile()

# Run the agent
if __name__ == "__main__":
    config = {"recursion_limit": config_data['run']['recursion_limit']}
    
    # Example 1: Simple question
    inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}
    for event in app.stream(inputs, config=config):
        for v in event.values():
            print(v["messages"][-1].content)

    print("\n---\n")

    # Example 2: Follow-up question
    inputs = {
        "messages": [
            HumanMessage(content="what is the weather in sf"),
            # The AI tool output now is part of the messages,
            # so the LLM can use it to generate a response.
            # This is a simplified example of how the conversation history is managed.
        ]
    }
    # In a real application, you would append the full tool output message.
    # For this example, we'll just re-run with the same input to show the flow.
    
    inputs = {"messages": [HumanMessage(content="what about in la?")]}
    for event in app.stream(inputs, config=config):
        for v in event.values():
            print(v["messages"][-1].content)

