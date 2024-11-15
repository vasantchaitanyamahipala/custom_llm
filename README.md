
Custom LLM 
![image](https://github.com/user-attachments/assets/2b1a8120-d98c-40ad-9276-84f599701100)

ChatGPT Response for the same question 
![image](https://github.com/user-attachments/assets/ec625261-fd5b-4412-ae7f-594885cb6572)







Custom LLM-Powered Assistant

This repository contains a project that builds a custom intelligent assistant powered by LLMs (Large Language Models) to assist contractors and builders in making informed decisions about building materials. The assistant integrates various technologies to handle natural language queries, recommend materials, answer technical questions, and provide specifications.
Features

    LLM-powered assistant using GPT-4.
    Retrieval-Augmented Generation (RAG) system for enhanced knowledge retrieval.
    Vector store integration using Chroma for efficient query processing.
    React-based frontend for user interaction.
    FastAPI backend for serving API requests.

Requirements

    Python 3.10 or later.
    Node.js and npm (for the frontend).
    Git for version control.
Set Up the OpenAI API Key

    Obtain your OpenAI API key from the OpenAI API platform.
    Export the API key as an environment variable

export OPENAI_API_KEY=your_api_key_here

Replace your_api_key_here with your actual API key.
The application will automatically read the API key from the environment. Ensure that the key is secure and not hardcoded into the codebase.

1. Clone the Repository
     git clone https://github.com/vasantchaitanyamahipala/custom_llm.git
     cd custom_llm

2. Python Environment Setup
    python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
3. Backend Setup
   cd ..
   uvicorn app:app --reload

4. cd frontend
   npm install
   npm start


Usage
Adding Documents to the Vector Store

    Use the embed.py script to add documents to the Chroma vector store:
    python embed.py

Interacting with the Assistant

    Open the frontend application in your browser (http://localhost:3000).
    Enter your query in the chat interface.
    The assistant will respond based on the integrated knowledge base and vector store.


API Endpoints
FastAPI Backend
Method	Endpoint	Description
POST	/chat	Processes user queries and returns assistant responses.
POST	/add-document	Adds a document to the vector store.


System Architecture

    Frontend: React-based UI for interacting with the assistant.
    Backend: FastAPI server for processing requests and managing interactions.
    Vector Store: Chroma database for document embeddings and retrieval.
    LLM: GPT-4 for processing and generating intelligent responses.


Here’s a structured and detailed README.md for your repository:
Custom LLM-Powered Assistant

This repository contains a project that builds a custom intelligent assistant powered by LLMs (Large Language Models) to assist contractors and builders in making informed decisions about building materials. The assistant integrates various technologies to handle natural language queries, recommend materials, answer technical questions, and provide specifications.
Features

    LLM-powered assistant using GPT-4.
    Retrieval-Augmented Generation (RAG) system for enhanced knowledge retrieval.
    Vector store integration using Chroma for efficient query processing.
    React-based frontend for user interaction.
    FastAPI backend for serving API requests.

Requirements

    Python 3.10 or later.
    Node.js and npm (for the frontend).
    Git for version control.

Setup Instructions
1. Clone the Repository

git clone https://github.com/vasantchaitanyamahipala/custom_llm.git
cd custom_llm

2. Python Environment Setup

    Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

Install the required Python dependencies:

    pip install -r requirements.txt
    
3. Backend Setup

    Return to the root directory of the repository:

cd ..

Start the FastAPI server:

    uvicorn app:app --reload

    The backend API will be available at http://127.0.0.1:8000.

4. Frontend Setup

    Navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the React development server:

    npm start

    The frontend should now be running at http://localhost:3000.


Usage
Adding Documents to the Vector Store

    Use the embed.py script to add documents to the Chroma vector store:

    python embed.py

    Provide the path to the document file when prompted.

Interacting with the Assistant

    Open the frontend application in your browser (http://localhost:3000).
    Enter your query in the chat interface.
    The assistant will respond based on the integrated knowledge base and vector store.

API Endpoints
FastAPI Backend
Method	Endpoint	Description
POST	/chat	Processes user queries and returns assistant responses.
POST	/add-document	Adds a document to the vector store.
System Architecture

    Frontend: React-based UI for interacting with the assistant.
    Backend: FastAPI server for processing requests and managing interactions.
    Vector Store: Chroma database for document embeddings and retrieval.
    LLM: GPT-4 for processing and generating intelligent responses.

Prompt Engineering

The system employs carefully crafted prompts to ensure that:

    Responses remain concise and relevant.
    Technical queries are answered with accuracy.
    Cost-effective recommendations are provided when applicable.



Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.
