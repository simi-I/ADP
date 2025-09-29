from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, session
from google.adk.runners import Runner
from google.genai.types import Content, Part
from dotenv import load_dotenv

load_dotenv()

greeting_agent = LlmAgent(
    name="Greeter",
    model="gemini-2.0-flash",
    instruction="Generate a short, friendly greeting",
    output_key="last_greeting"
)

# Setup Runner and session

app_name, user_id, session_id = "state_app", "user1", "session1"
session_service = InMemorySessionService()

runner = Runner(
    agent=greeting_agent, 
    app_name=app_name,
    session_service=session_service
)

session = session_service.create_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id
)

# print(f"Initial state: {}")

# Run the agent
user_message = Content(parts=[Part(text="Hello")])
print("\n--- Running the agent ---")
for event in runner.run(
    user_id=user_id,
    session_id=session_id,
    new_message=user_message
):
    if event.is_final_response():
        print("Agent responded")

updated_session = session_service.get_session(app_name, user_id, session_id)
print(f"\n State afrer agent run: {updated_session.state}")