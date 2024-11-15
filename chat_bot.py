import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor


# Get the API key from the environment variable
openai_api_key = ""


if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.5,
    max_tokens=400,
    api_key=openai_api_key  )

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create embeding model
embedings = OpenAIEmbeddings(api_key=openai_api_key)  

# Initialize Chroma DB (vector database)
vector_db = Chroma(embedding_function=embedings, collection_name="my_collection", persist_directory="./chroma_db")

# Create a ContextualCompressionRetriever
retriever = ContextualCompressionRetriever(
    base_compressor=LLMChainExtractor.from_llm(llm),
    base_retriever=vector_db.as_retriever()
)

# Create a template for combining the memory, database, and LLM

# Custom prompt for construction-focused assistant
prompt_template = ChatPromptTemplate.from_template("""

                                                   
Respond to the following question:
Context: {context}
Chat History: {chat_history}
Human: {question}
AI:
""")



# Create the ConversationalRetrievalChain
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt_template}
)

def chatbot_response(user_input):
    # Get the response based on user input
    try:
        return conversation_chain({"question": user_input})["answer"]
    except Exception as e:
        return f"Error: {e}"

