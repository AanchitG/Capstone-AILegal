# Capstone project of Aanchit Govind

# AI-Powered Legal Document Review System

## Project Overview
This project implements a multi-agent AI system designed to review legal documents, flag compliance issues, and generate grounded summaries using Retrieval-Augmented Generation (RAG) and Semantic Kernel. It leverages Azure services for storage, search, orchestration, and monitoring. 

## PPT with Agent Workflow and System Architecture details uploaded in repository

## Features
- Document ingestion from Azure Blob Storage
- Clause extraction using OpenAI
- Compliance validation with confidence scoring
- Retrieval of similar clauses via Azure Cognitive Search
- Grounded summarization using RAG
- Agent orchestration via Azure AI Foundry
- Monitoring and logging of agent decisions

## Architecture Diagram
Refer to the architecture diagram image included in the repository for a visual representation of the system.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/legal-doc-review-system.git
   cd legal-doc-review-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following variables:
   ```env
   AZURE_STORAGE_CONNECTION_STRING=your_connection_string
   AZURE_SEARCH_ENDPOINT=your_search_endpoint
   AZURE_SEARCH_API_KEY=your_search_api_key
   AZURE_SEARCH_INDEX_NAME=your_index_name
   AZURE_OPENAI_ENDPOINT=your_openai_endpoint
   AZURE_OPENAI_API_KEY=your_openai_api_key
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   AZURE_FOUNDRY_PROJECT_ENDPOINT=your_foundry_endpoint
   AZURE_FOUNDRY_PROJECT_API_KEY=your_foundry_api_key
   AZURE_FOUNDRY_PROJECT_MODEL_ID=your_model_id
   ```

## How to Run
1. **Ingest documents to Azure Search**:
   ```bash
   python ingest_to_search.py
   ```

2. **Run the main agent pipeline**:
   ```bash
   python main_agent.py
   ```

## Technologies Used
- Python 3
- Azure Blob Storage
- Azure Cognitive Search
- Azure OpenAI
- Azure AI Foundry
- LangChain
- Semantic Kernel
- FastAPI
