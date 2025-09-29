from google.adk.tools import google_search
from google.adk.agents import Agent

search_agent = Agent(
    name= "research_assistant",
    model="gemini-2.0-flash-exp",
    instruction="You help users research topics. When asked, use the google search tool",
    tools=[google_search]
)

