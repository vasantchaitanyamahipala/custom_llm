import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from chat_bot import chatbot_response
from fastapi.middleware.cors import CORSMiddleware
import json
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
def generate_event(user_input):

    for token in chatbot_response(user_input, stream_to_terminal=False):
        data= json.dumps({"message": token})
        yield f"data: {data}\n\n" 
    yield "event: end\n{} \n\n"    



@app.post("/")
@app.post("/chat")
async def root(input: MessageRequest):
    user_input = input.message
    print(user_input)
    if not user_input:
        raise HTTPException(status_code=400, detail="Message is empty")
    try:
        
        return StreamingResponse(
        generate_event(user_input),
        media_type="text/event-stream"
    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


