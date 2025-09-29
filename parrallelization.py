import os
import asyncio
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    llm = ChatGroq(
        model = "llama-3.1-8b-instant",
    )
    
except Exception as e:
    print(f" Error initializing language model: {e}")
    llm = None

# define Independent Chains 

summarize_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Summarize the following topic concisely:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

questions_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Generate three interesting questions about the following topic:"),
        ('user', "{topic}")
    ])
    | llm
    | StrOutputParser()
)

terms_chain: Runnable =(
    ChatPromptTemplate.from_messages([
        ("system", "Identify 5-10 key terms from the following topic, seperated by comas:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

# Build the parallel + synthesis chain

map_chain = RunnableParallel({
    "summary" : summarize_chain,
    "questions" : questions_chain,
    "key_terms" : terms_chain,
    "topic" : RunnablePassthrough(), 
})

synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", """ Based on the following information:
     Summary: {summary}
     Related Questions: {questions}
     Key terms: {key_terms}
     Synthesize a comprehensive answer.
     """),
    ("user", "Orginal topic: {topic}")
])

full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()

async def run_parallel_example(topic: str) -> None : 
    """Asynchronously invokes the parallel processing chain with a specific topic
   and prints the synthesized result.

   Args:
       topic: The input topic to be processed by the LangChain chains.
    """
    if not llm:
        print("LLM not initialized. Cannot run example.")
        return
    print(f"\n--- Running Parallel Langchain Example for topic: '{topic}'")
    try:
        response = await full_parallel_chain.ainvoke(topic)
        print("\n Final response")
        print(response)
    except Exception as e:
        print(f"\n An error occured during chain excecution: {e}")
        
if __name__ == "__main__":
    test_topic = "The history of space exploration"
    asyncio.run(run_parallel_example(test_topic))