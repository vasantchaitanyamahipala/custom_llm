import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

# OpenAI API Key
openai_api_key = ""

# Initialize embeddings and vector database
embeddings = OpenAIEmbeddings(api_key=openai_api_key)
vector_db = Chroma(embedding_function=embeddings, collection_name="my_collection", persist_directory="./chroma_db")

def add_document_to_chroma(file_path):
    """
    Load a document, split it into smaller chunks, and add them to the Chroma vector database.
    """
    try:
        print(f"Loading file: {file_path}")

        loader = TextLoader(file_path)
        doc = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        text_chunks = text_splitter.split_documents(doc)

        vector_db.add_documents(text_chunks)
        print(f"Added {len(text_chunks)} text chunks from {file_path} to the vector database.")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main():

    print("Welcome to the Document ChromaDB Loader!")
    print("Enter 'q' to quit.")
    
    while True:
        file_path = input("Enter the file path to add to the vector database: ").strip()
        
        if file_path.lower() == "q":
            print("Exiting the program. Goodbye!")
            break

        if os.path.exists(file_path):
            add_document_to_chroma(file_path)
        else:
            print(f"File '{file_path}' does not exist. Please try again.")

if __name__ == "__main__":
    main()
