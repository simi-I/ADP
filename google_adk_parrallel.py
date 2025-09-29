from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

GEMINI_MODEL = "gemini-2.0-flash"

# -- 1. Define Researcher Sub-Agents (to run in parallel)

researcher_agent1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model = GEMINI_MODEL,
    instruction="""
    You are an AI Research Assistant specializing in energy.
Research the latest advancements in 'renewable energy sources'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
    """,
    description="Researches renewable energy sources. ",
    tools=[google_search],
    output_key="renewable_energy_result"
)

researcher_agent_2 = LlmAgent(
    name="EVResearcher", 
    model=GEMINI_MODEL, 
    instruction="""
    You are an AI Research Assistant specializing in transportation.
Research the latest developments in 'electric vehicle technology'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
    """,
    description="Researches electric vehicle technology",
    tools=[google_search],
    output_key="ev_technology_result"
)

researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher", 
    model = GEMINI_MODEL, 
    instruction="""
    You are an AI Research Assistant specializing in climate solutions.
Research the current state of 'carbon capture methods'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches carbon capture methods.", 
    tools=[google_search],
    output_key="carbon_capture_result"
)

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent1, researcher_agent_2, researcher_agent_3], 
    description="Runs multiple research agents in parallel to gather information"
)

merger_agent = LlmAgent(
    name="SynthesisAgent",
    model = GEMINI_MODEL, 
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.
Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas. Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.

**Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

**Input Summaries:**

*   **Renewable Energy:**
    {renewable_energy_result}
*   **Electric Vehicles:**
    {ev_technology_result}
*   **Carbon Capture:**
    {carbon_capture_result}

**Output Format:**

## Summary of Recent Sustainable Technology Advancements

### Renewable Energy Findings
(Based on RenewableEnergyResearcher's findings)
[Synthesize and elaborate *only* on the renewable energy input summary provided above.]

### Electric Vehicle Findings
(Based on EVResearcher's findings)
[Synthesize and elaborate *only* on the EV input summary provided above.]

### Carbon Capture Findings
(Based on CarbonCaptureResearcher's findings)
[Synthesize and elaborate *only* on the carbon capture input summary provided above.]

### Overall Conclusion
[Provide a brief (1-2 sentence) concluding statement that connects *only* the findings presented above.]

Output *only* the structured report following this format. Do not include introductory or concluding phrases outside this structure, and strictly adhere to using only the provided input summary content.
""",
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs. ", 

)

sequentail_pipeline_agent = SequentialAgent(
    name="ResearchAndSythesisPipeline", 
    sub_agents=[parallel_research_agent, merger_agent],
    description="Coordinates parallel research and synthesizes the results"
)

root_agent = sequentail_pipeline_agent