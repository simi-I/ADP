import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
        model = "groq/llama-3.1-8b-instant",
        temperature= 0.1
)

planner_writer_agent = Agent(
    role='Article Planner and Writer',
    goal = 'Plan and then write a concise, engaging summary on a specified topic',
    backstory=(
        'You are an expert technical writer and content strategist'
        'Your strength lies in creating a clear, actionable plan before writing, '
        'ensuring the final summary is both informative and east to digest.'
    ),
    verbose=True, 
    allow_delegation=False, 
    llm=llm
)

topic = "The importance of Reinforcement Learning in AI"
high_level_task = Task(
    description=(
        f"1. Create a bullet-point plan for a summary on the topic: '{topic}'. \n"
        f"2. Write the summary based on your plan, keeping it around 200 words"
    ),
    expected_output=(
        "A final report containing two distinct sections:\n\n"
       "### Plan\n"
       "- A bulleted list outlining the main points of the summary.\n\n"
       "### Summary\n"
       "- A concise and well-structured summary of the topic."
    ),
    agent= planner_writer_agent,
)

# create the crew with a clear process
crew = Crew(
    agents=[planner_writer_agent],
    tasks=[high_level_task],
    process=Process.sequential,
)

# if __name__ == "__main__":
print("Running the planning and writing task")
result = crew.kickoff()

print("Task Results")
print(result)