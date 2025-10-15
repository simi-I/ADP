import os
import requests
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GOOGLE_CUSTOM_SEARCH_API_KEY = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not GOOGLE_CUSTOM_SEARCH_API_KEY or not GOOGLE_CSE_ID:
    raise ValueError(
        "Please set keys in your .env file"
    )
    
def create_groq(model:str):
    return ChatGroq(
        model = model, 
        temperature = 0.1
    )

client = create_groq(model="llama-3.3-70b-versatile")

# --- step 1: Classify the prompt ---

def classify_prompt(prompt: str) -> dict:
    system_message = {
        "role" : "system",
        "content":(
            "You are a classifier that analyzes user prompts and returns one of three categories Only: \n\n"
            "- Simple\n"
            "- reasoning\n"
            "- internet_search\n\n"
            "Rules:\n"
            "- Use 'simple' for direct factual questions that need no reasoning or current events. \n"
            "- Use 'reasoning' for logic, math, or multi-step inference questions. \n"
            "- Use 'internet_search' if the prompt refers to current events, recent data, or things not in your training data. \n\n"
            "Respond Only with Json like:\n"
            '{"classification":"simple"}'
        ),
    }
    
    user_message = {"role":"user", "content": prompt}
    
    response = client.invoke([system_message, user_message])
    content = response.content
    
    return json.loads(content)

# -- step 2: Google search ---
def google_search(query: str, num_results = 1) -> list:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_CUSTOM_SEARCH_API_KEY,
        "cx" : GOOGLE_CSE_ID,
        "q" : query,
        "num": num_results,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        
        if "items" in results and results["items"]:
            return [
                {
                    "title": item.get("title"),
                    "snippet": item.get("snippet"),
                    "link": item.get("link"),
                }
                for item in results["items"]
            ]
        else:
            return []
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
# --- Step 3: Generate Response ---
def generate_response(prompt: str, classification: str, search_results=None) -> str:
    if classification == "simple":
        model = "llama-3.3-70b-versatile"
        full_prompt = prompt
    elif classification == "reasoning":
        model = "openai/gpt-oss-120b"
        full_prompt = prompt
    elif classification == "internet_search":
        model = "openai/gpt-oss-20b"
        # Convert each search result dict to a readable string 
        if search_results:
            search_context = "\n".join(
                [
                    f"Title: {item.get('title')}\nSnippet:{item.get('snippet')}\nLink: {item.get('link')}"
                    for item in search_results
                ]
            )
        else:
            search_context = "No search results found."
        full_prompt = f"""
        Use the following web results to answer the user query:
        {search_context}
        Query: {prompt}        
        """
    client = create_groq(model=model)    
    response = client.invoke([{"role":"user", "content": full_prompt}])
    
    return response.content, model

# --- Step 4: Combined Router ---
def handle_prompt(prompt: str) -> dict:
    classification_result = classify_prompt(prompt)
    classification = classification_result["classification"]
    
    search_results = None 
    if classification == "internet_search":
        search_results = google_search(prompt)
        print("\n Search Results:", search_results)
        
    answer, model = generate_response(prompt, classification, search_results)
    
    return {"classification": classification, "response": answer, "model": model}

#test_prompt = "What is the Capital of Australia?"
#test_prompt = "Explain the impact of quantum computing on cryptography."
test_prompt = "When does the australian open 2026 start, give me full date?"

result = handle_prompt(test_prompt)
print("Classification:", result["classification"])
print("Model Used:", result["model"])
print("Response:\n", result["response"]) 






