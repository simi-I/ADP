import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    max_tokens=512
)

# prompt 1: Extract information
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

# prompt 2: Transform to JSON
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys: \n\n{specifications}  " 
)

extraction_chain = prompt_extract | llm | StrOutputParser()

full_chain = (
    {"specifications" : extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

# Run the chain
input_text = "The new laptop model features a 3.5 GHZ octa-core processor, 16GB of RAM and a 1TB NVMe SSD."

def main():
    # Execute the chain with the input text dictionary.
    final_result = full_chain.invoke({"text_input": input_text})

    print('\n -- Final JSON Output')
    print(final_result)
    

if __name__ == "__main__":
    main()