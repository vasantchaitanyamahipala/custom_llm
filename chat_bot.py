from transformers import GPT2Tokenizer
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import Document
import threading
import queue

# Initialize GPT-2 tokenizer (compatible with OpenAI models)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Get the API key from the environment variable
openai_api_key = ""

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.8,
    max_tokens=1000,
    api_key=openai_api_key,
    streaming=True
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create embedding model
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Initialize Chroma DB (vector database)
vector_db = Chroma(embedding_function=embeddings, collection_name="my_collection", persist_directory="./chroma_db")

# Add example documents to vector DB
documents = [
    Document(page_content="Concrete is widely used for construction projects due to its durability.", metadata={"type": "construction"}),
    Document(page_content="Steel reinforcement provides strength in building structures.", metadata={"type": "construction"})
]
vector_db.add_documents(documents)

# Create a ContextualCompressionRetriever
retriever = ContextualCompressionRetriever(
    base_compressor=LLMChainExtractor.from_llm(llm),
    base_retriever=vector_db.as_retriever(),
)

# Create a template for combining the memory, database, and LLM
prompt_template = ChatPromptTemplate.from_template("""
You are a highly knowledgeable assistant specializing in construction materials and techniques. Your role is to:
1. Understand and respond in the context of construction and building projects.
2. Recommend appropriate materials for various use cases.
3. Provide detailed technical specifications when requested.
4. Maintain a focus on cost-effectiveness, including providing price ranges and budget-conscious options.
5. Provide a concise, clear, and well-structured answer. Use bullet points or numbered lists where appropriate.

Important Instructions:
- Do not use any fancy formatting, such as bold, italics, or underlining.
- Avoid highlighting and Keep the response in plain text.
- Keep the output in plain text, with simple bullet points or numbered lists if needed.
- Ensure your output is formatted correctly for easy reading and comprehension.

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
    combine_docs_chain_kwargs={"prompt": prompt_template},
)

class TokenStreamHandler(BaseCallbackHandler):
    def __init__(self, stream_to_terminal=True):
        self.queue = queue.Queue()
        self.capture_tokens = False  
        self.temp=[]

    def on_llm_new_token(self, token: str, **kwargs) -> None:
            print(f"Additional arguments (kwargs): {kwargs}")
            tags = kwargs.get("tags", [])
            if tags :
                self.capture_tokens = True

            if not tags and self.capture_tokens:
                self.queue.put(token)
                self.temp.append(token)
 
    def get_tokens(self):
        while True:
            token= self.queue.get()
            if token is None:
                break
            yield token
        


def chatbot_response(user_input, stream_to_terminal=True):
    handler= TokenStreamHandler(stream_to_terminal)
    thread = threading. Thread (target=conversation_chain, args=({"question": user_input}, ), kwargs={"callbacks": [handler]})
    thread.start()
    for token in handler.get_tokens():
        yield token
    
    thread.join()
    handler.queue.put(None)