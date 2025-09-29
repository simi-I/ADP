import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

def setup_environment():
    """
    Loads environment variables and checks for the required API key
    """
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file. ")
    
    
def main():
    """
    Initializes and runs the AI crew for content creation using the latest Gemini model.
    """
    
    setup_environment()
    
    llm = ChatGroq(
        model = "groq/llama-3.1-8b-instant",
        temperature= 0.1
)
    
    researcher = Agent(
        role="Senior Research Analyst",
        goal='Find and Summarize the latest trends in AI.',
        backstory="You are an experienced research analyst with a knack for identifying key trends and synthesizing information",
        verbose=True, 
        allow_delegation=False, 
        llm=llm
    )
    
    writer = Agent(
        role='Technical Content Writer',
        goal='Write a clear and engaging blog post based on research findings',
        backstory='You are a skilled writer who can translate complex technical topics into accessible content',
        verbose=True, 
        allow_delegation=False,
        llm=llm
    )
    
    research_task = Task(
        description="Research the top 3 emerging trends in Artificial Intelligence in 2024-2025. Focus on practical applications and potential impact.",
        expected_output="A detailed summary of the top 3 AI trends, including key points and sources",
        agent=researcher,
        
    )
    
    writing_task = Task(
        description="Using the research findings from the previous task, Write a 500-word blog post based on the research findings: {research_task}. The post should be engaging and easy for a general audience to understand.",
        expected_output="A complete 500-word blog post about the latest AI trends.",
        agent=writer, 
        context=[research_task],
    )
    
    blog_creation_crew = Crew(
        agents = [researcher, writer],
        tasks = [research_task, writing_task],
        process = Process.sequential,
        verbose = True
    )
    print("Running the blog creation crew with Gemini 2.0 Flash")
    
    try:
        result = blog_creation_crew.kickoff()
        print("\n ------------ \n")
        print("Crew final Output")
        print(result)
    except Exception as e:
        print(f"\n An unepected error occured: {e}")
        
if __name__ == "__main__":
    main()