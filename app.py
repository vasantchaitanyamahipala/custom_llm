import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chat_bot import chatbot_response
from fastapi.middleware.cors import CORSMiddleware
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

def preprocess_response(response: str) -> str:
    # Remove Markdown formatting
    response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)  # Remove bold
    response = re.sub(r'\*(.*?)\*', r'\1', response)      # Remove italics
    response = re.sub(r'`(.*?)`', r'\1', response)        # Remove inline code
    response = re.sub(r'~~(.*?)~~', r'\1', response)      # Remove strikethrough
    response = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', response)  # Remove links
    response = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', response) # Remove images
    response = re.sub(r'#+ ', '', response)               # Remove headers
    response = re.sub(r'> ', '', response)                # Remove blockquotes
    response = re.sub(r'\n\s*\n', '\n', response)         # Remove extra newlines

    # Clean up numbered lists and hyphens
    response = re.sub(r"(\d+\.)", r"\n\1", response)  # Add newline before numbered lists
    response = re.sub(r"-", "- ", response)

    # Ensure paragraphs are separated by new lines
    response = re.sub(r'(\.)(\s+)(\d+\.)', r'\1\n\n\3', response)  # Add newline after periods before new numbers
    response = re.sub(r'(\.)(\s+)(-)', r'\1\n\n\3', response)  # Add newline after periods before hyphens

    # Add newlines after each period followed by a capital letter (indicating a new sentence)
    response = re.sub(r'(\.)(\s+)([A-Z])', r'\1\n\n\3', response)

    return response.strip()



@app.post("/")
@app.post("/chat")
async def root(input: MessageRequest):
    user_input = input.message
    if not user_input:
        raise HTTPException(status_code=400, detail="Message is empty")
    try:
        raw_response = chatbot_response(user_input)
        processed_response = preprocess_response(raw_response)
        return {"response": processed_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


