import os 
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    max_tokens=512
)

def booking_handler(request: str) -> str:
    """Simulates the booking Agent handling a request"""
    print("\n-- Delegating to booking handler ---")
    return f"Booking Handler processed request: '{request}', Result: Simulated booking action."

def info_handler(request: str) -> str:
    """Simulates the info agent handling a request."""
    print("\n-- Delegating to Info Handler")
    return f"Info Handler processed request: '{request}'. Result: Simulated Information retrieval"

def unclear_handler(request: str) -> str:
    """Handles request that couldnt be delegated. """
    print("\n-- Handling Unclear request")
    return f"Coordinator could not delegate request: '{request}'. Please Clarify"

coordinator_router_prompt = ChatPromptTemplate.from_messages([
   ("system", """Analyze the user's request and determine which specialist handler should process it.
    - If the request is related to booking flights or hotels, 
      output 'booker'.
    - For all other general information questions, output 'info'.
    - If the request is unclear or doesn't fit either category, 
      output 'unclear'.
    ONLY output one word: 'booker', 'info', or 'unclear'."""),
   ("user", "{request}")
])

if llm:
    coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()
    
branches = {
    "booker" : RunnablePassthrough.assign(output=lambda x: booking_handler(x['request']['request'])),
    
    "info" : RunnablePassthrough.assign(output=lambda x: info_handler(x['request']['request'])),
    
    "unclear" : RunnablePassthrough.assign(output=lambda x: unclear_handler(x['request']['request'])),
}

delegation_branch = RunnableBranch(
    (lambda x: x['decision'].strip() == 'booker', branches["booker"]),
    (lambda x: x['decision'].strip() == 'info', branches["info"]),
    branches["unclear"] 
)

coordinator_agent = {
    "decision": coordinator_router_chain,
    "request": RunnablePassthrough()
} | delegation_branch | (lambda x: x['output'])

def main():
    if not llm:
        print("\n Skipping execution due to LLM Initialization failure")
        return 
    
    print("--- Running with a booking request ---")
    request_a = "Book me a flight to London."
    result_a = coordinator_agent.invoke({"request": request_a})
    print(f"Final Result A: {result_a}")

    print("\n--- Running with an info request ---")
    request_b = "What is the capital of Italy?"
    result_b = coordinator_agent.invoke({"request": request_b})
    print(f"Final Result B: {result_b}")

    print("\n--- Running with an unclear request ---")
    request_c = "Tell me about quantum physics."
    result_c = coordinator_agent.invoke({"request": request_c})
    print(f"Final Result C: {result_c}")

if __name__ == "__main__":
    main()