import time
from chat_bot import TokenStreamHandler  # Import your class

def mock_token_generator(handler):
    """
    Simulates the behavior of a token generator like LangChain.
    """
    tokens = ["The", "capital", "of", "India", "is", "New", "Delhi", "."]
    for token in tokens:
        handler.on_llm_new_token(token)  # Add token to the queue
        time.sleep(0.5)  # Simulate delay between tokens
    handler.finish()  # Mark the stream as finished
