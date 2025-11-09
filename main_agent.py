from dotenv import load_dotenv
import os
import logging
from typing import List
import openai
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

# Configure OpenAI for Azure
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_version = "2024-05-01-preview"

# Setup logging
logging.basicConfig(filename='agent_logs.txt', level=logging.INFO)

def extract_clauses(document_text: str) -> List[str]:
    response = openai.ChatCompletion.create(
        engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a legal clause extraction assistant."},
            {"role": "user", "content": f"Extract all legal clauses from the following document:\n\n{document_text}"}
        ]
    )
    return response['choices'][0]['message']['content'].split("\n")

def validate_clause(clause: str) -> str:
    prompt = f"Analyze the following clause for compliance issues. Return any flagged issues and a confidence score (0-1):\n\n{{clause}}"
    response = openai.ChatCompletion.create(
        engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a legal compliance validation assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def retrieve_similar_clauses(query: str) -> List[str]:
    search_client = SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
    )
    results = search_client.search(search_text=query, top=5)
    return [doc['content'] for doc in results if 'content' in doc]

def generate_summary_with_rag(query: str) -> str:
    context_clauses = retrieve_similar_clauses(query)
    context = "\n".join(context_clauses)
    prompt = f"Based on the following clauses:\n{context}\n\nProvide a grounded summary for the query:\n{query}"
    response = openai.ChatCompletion.create(
        engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a legal assistant that provides grounded summaries using retrieved legal clauses."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def run_pipeline(document_path: str):
    with open(document_path, "r") as f:
        text = f.read()

    clauses = extract_clauses(text)

    for clause in clauses:
        print("\n--- Clause ---")
        print(clause)
        validation = validate_clause(clause)
        print("Validation:", validation)
        logging.info(f"Clause: {clause}\nValidation: {validation}\n")

    query = "What are the compliance risks in the document?"
    summary = generate_summary_with_rag(query)
    print("\n--- RAG Summary ---")
    print(summary)

if __name__ == "__main__":
    run_pipeline("sample_document.txt")