import os
import random
import re
from pathlib import Path
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    temperature=0.3
)

# Utility functions

def generate_prompt(
    use_case: str, goals: list[str], previous_code: str ="", feedback: str= ""
) -> str:
    print("Constructing prompt for code generation...")
    base_prompt = f"""
    You are an AI coding agent. Your job is to write python code based on the following use case:
    Use case: {use_case}
    
    your goals are:
    {chr(10).join(f"- {g.strip()}" for g in goals)}
    """
    if previous_code:
        print("Adding previous code to the prompt for refinement.")
        base_prompt += f"\n Previously generated code: \n{previous_code}"
    if feedback:
        print("Including feedback fore revision. ")
        base_prompt += f"\n Feedback on previous version: \n{feedback}\n"
        
    base_prompt += "\n Please return only the revised Python code. DO not include comments or explanations outside the code"
    return base_prompt

def get_code_feedback(code: str, goals: list[str]) -> str:
    print("Evaluating code against the goals...")
    feedback_prompt = f"""
    you are a python code reviewer. A code snippet is shown below. Based on the following goals:
    {chr(10).join(f"- {g.strip()}" for g in goals)}
    
    please critique this code and identify if the goals are met. Meniton if improvements are needed for clarity, simplicity, correctness, edge case handling, or test coverage.
    Code:
    {code}
    """
    return llm.invoke(feedback_prompt)

def goals_met(feedback_text: str, goals: list[str]) -> bool:
    """
    Uses the LLM to evaluate Whether the goals have been met based on the feedback text. 
    Returns True or False (parsed from LLM output).
    """
    review_prompt = f"""
    You are an AI reviewer.
    Here are the goals:
    {chr(10).join(f"-{g.strip()}" for g in goals)}
    
    Here is the feedback on the code:
    \"\"\"
    {feedback_text}
    \"\"\"
    Based on the feedbacj above, have the goals been met?
    Respond with only one word: True or False.
    """
    
    response = llm.invoke(review_prompt).content.strip().lower()
    return response == "true"
    
def clean_code_block(code: str) -> str:
    lines = code.strip().splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()

def add_comment_header(code: str, use_case: str) -> str:
    comment = f"# This Python program implements the following use case:\n# {use_case.strip()}\n"
    return comment + "\n" + code

def to_snake_case(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]", "", text)
    return re.sub(r"\s+", "_", text.strip().lower())

def save_code_to_file(code: str, use_case: str) -> str:
    print("Saving final code to file...")
    
    summary_prompt = (
        f"Summarize the following use case into a single lowercase word or phrase,"
        f"no more than 10 characters, suitable for a Python filename:\n\n{use_case}"
    )
    raw_summary = llm.invoke(summary_prompt).content.strip()
    short_name = re.sub(r"[^a-zA-Z0-9_]", "", raw_summary.replace(" ", "_").lower())[:10]
    
    random_suffix = str(random.randint(1000, 9999))
    filename = f"{short_name}_{random_suffix}.py"
    filepath = Path.cwd() / filename
    
    with open(filepath, "w") as f:
        f.write(code)
        
    print(f"Code saved to: {filepath}")
    return str(filepath)


# -- Main Agent Function ---
def run_code_agent(use_case: str, goals_input: str, max_iterations: int = 5) -> str:
    goals = [g.strip() for g in goals_input.split(",")]
    
    print(f"\n Use Case: {use_case}")
    print("Goals")
    for g in goals:
        print(f"    - {g}")
        
    previous_code = ""
    feedback = ""
    
    for i in range(max_iterations):
        print(f"\n=== Iteration {i + 1} of {max_iterations} ===")
        prompt = generate_prompt(use_case, goals, previous_code, feedback if isinstance(feedback, str) else feedback.content)
        
        print("Generating code..")
        code_response = llm.invoke(prompt)
        raw_code = code_response.content.strip()
        code = clean_code_block(raw_code)
        print("\n Generared Code: \n" + "-" * 50 + f"\n{code}\n" + "-" * 50)
        
        print("\n Submitting code for feedback review...")
        feedback = get_code_feedback(code, goals)
        feedback_text = feedback.content.strip()
        print("\n Feedback Received:\n" + "-" * 50 + f"\n{feedback_text}\n" + "-" * 50)
        
        if goals_met(feedback_text, goals):
            print("LLM confirms goal are met. stopping iteration")
            break
        
        print("Goals not fully met. Preparing for next iteration...")
        previous_code = code
    
    final_code = add_comment_header(code, use_case)
    return save_code_to_file(final_code, use_case)


if __name__ == "__main__":
    print("\n Welcome to the AI code Generation Agent")
    
    #Example 1
    use_case_input = "Write code to find BinaryGap of a given positive integer"
    goals_input = "Code simple to understand, functionally correct, handles comprehensice edge cases, takes postive integer input only, prints the results with few examples"
    
    run_code_agent(use_case_input, goals_input)
    
    # Examples 2
    use_case_input = "Write code to count the number of files in current directory and all its nested sub_directories and print the total count"
    goals_input = (
        "Code simple to understand, functionally correct, handles comprehensive edge cases, ignore recommendations for performance, ignore recommendations for test suite use like unittest or pytest"
    )
    run_code_agent(use_case_input, goals_input)
    
    # Example 3
    use_case_input = "Write code which takes a command line input of a word doc or docx file and opens it and counts the number of words, and characters in it and prints all"
    goals_input = "Code simple to understand, functionally correct, Handkes edge cases"
    run_code_agent(use_case_input, goals_input)
    
        
    