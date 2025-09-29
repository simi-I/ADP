import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    llm = ChatGroq(
        model = "llama-3.1-8b-instant",
    )
    
except Exception as e:
    print(f" Error initializing language model: {e}")
    llm = None
    
def run_reflection_loop():
    """
    Demonstrates a multi-step AI reflection loop to progressively imporve a Python Function
    """
    task_prompt = """
    Your task is to create a Python function named `calculate_factorial`.
    This function should do the following:
    1.  Accept a single integer `n` as input.
    2.  Calculate its factorial (n!).
    3.  Include a clear docstring explaining what the function does.
    4.  Handle edge cases: The factorial of 0 is 1.
    5.  Handle invalid input: Raise a ValueError if the input is a negative number.
    """
    # --- Reflection loop
    max_iterations = 3
    current_code = ""
    
    message_history = [HumanMessage(content=task_prompt)]
    
    for i in range(max_iterations):
        print("\n" + "="*25 + f"Reflection Loop: Iteration{i + 1}" + "="*25)
        if i == 0:
            print("\n >>> Stage 1: Generating initial code...")
            response = llm.invoke(message_history)
            current_code = response.content
        else:
            print("\n>>> STAGE 1: REFINING Code based on previous critique..")
            message_history.append(HumanMessage(content="Please refine the code using the critiques provided. "))
            response = llm.invoke(message_history)
            current_code = response.content
        print("\n--- Generated code (v" + str(i+1) + ") --\n" + current_code)
        message_history.append(response)
        
        print("\n>>> STAGE 2: REFLECTING on the generated code...")
        
        reflector_prompt = [
            SystemMessage(content="""
                        You are a senior software engineer and an expert 
                        in Python.
                        Your role is to perform a meticulous code review.
                        Critically evaluate the provided Python code based 
                        on the original task requirements.
                        Look for bugs, style issues, missing edge cases, 
                        and areas for improvement.
                        If the code is perfect and meets all requirements,
                        respond with the single phrase 'CODE_IS_PERFECT'.
                        Otherwise, provide a bulleted list of your critiques.
                          """),
            HumanMessage(content=f"Original Task:\n{task_prompt}\n\nCode to Review:\n{current_code}")
        ]
        
        critique_response = llm.invoke(reflector_prompt)
        critique = critique_response.content
        
        # --- STOPPING CONDITION
        
        if "CODE_is_PERFECT" in critique:
            print("\n--- Critique ---\n NO further critiques found. The code is satisfactory. ")
            break
        
        print("\n-- Critique --\n" + critique)
        message_history.append(HumanMessage(content=f"Critique of the previous code:\n{critique}"))
    print("\n" + "="*30 + " FINAL RESULT " + "="*30)
    print("\n Final refined code after the reflection proces: \n")
    print(current_code)

if __name__ == "__main__":
    run_reflection_loop()
    
    
        