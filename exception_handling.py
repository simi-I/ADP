from google.adk.agents import Agent, SequentialAgent

# Agent 1: Tries the primary tool. Its focus is narrow and clear

primary_handler = Agent(
    name="primary_handler",
    model="gemini-2.0-flash-exp",
    instruction="""
    Your job is to get precise location information
    Use the get_precise_location_info tool with the user's provided address
    """,
    tools = [get_precise_location_info]
)

# agent 2: Acts as the fallback handler, checking state to decide its action

fallback_handler = Agent(
    name="fallback_handler",
    model="gemini-2.0-flash-exp",
    instruction="""
    Check if the primary location lookup failed by looking at state["primary_location_failed"],
    - if it is True, extract the city from the user's orginal query and use the general_are_info tool.
    - if it is False, do nothing.
    """,
    tools = [get_general_area_info]
)

# Agent 3: Present the final result from the state
response_agent = Agent(
    name="response_agent",
    model= "gemini-2.0-flash-exp",
    instruction="""
    Review the location information store in state["location_result"].
    if state["location_result"] does not exisit or is empty, apologise
    that you could not retrieve the location
    """,
    tools=[]
)

robust_location_agent = SequentialAgent(
    name="robust_location_agent",
    sub_agents=[primary_handler, fallback_handler, response_agent]
)