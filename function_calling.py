import os, getpass
import asyncio
import nest_asyncio
from typing import List
from dotenv import load_dotenv
import logging

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    llm = ChatGroq(
        model = "llama-3.1-8b-instant",
        temperature= 0.1
    )
    
except Exception as e:
    print(f" Error initializing language model: {e}")
    llm = None
    
@langchain_tool
def search_information(query: str) -> str:
    """
    Provides factual information on a given topic. Use this tool to find answers to phrases like 'capital of France' or 'weather in London?'.
    """
    print(f"\n --- Tool called: search_information with query: '{query}' ---")
    simulated_results = {
        "weather in london": "The weather in London is currently cloudy with a temperature of 15 C",
        "capital of france": "The capital of france is Paris. ",
        "population of earth" : "The estimated population of Earth is around 8 bullion people.",
        "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
        "default": f"Simulated search result for '{query}': Np specific information found, but the topic seems interesting. "
    }
    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- Tool Result: {result} ---")
    return result

tools = [search_information]

# --- Create a Tool calling agent 
if llm:
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
        ('placeholder', "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, agent_prompt)
    agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)


async def run_agent_with_tool(query: str):
    """
    Invokes the agent executor with a query and prints the final response.
    """
    print(f"\n-- Running Agent with Query: '{query}' ---")
    try:
        response = await agent_executor.ainvoke({"input": query})
        print("\n--- Final Agent Response ---")
        print(response["output"])
    except Exception as e:
        print(f"\n An error occured during agent execution: {e}")

async def main():
    """Runs all agent queries concurrently"""
    tasks = [
        run_agent_with_tool("What is the capital of France?"),
        run_agent_with_tool("what's weather like in London?"),
        run_agent_with_tool("Tell me something about dogs.")
    ]
    await asyncio.gather(*tasks)
    
# if __name__ == "__main__":
nest_asyncio.apply()
asyncio.run(main())
