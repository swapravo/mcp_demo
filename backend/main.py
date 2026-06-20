import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
from typing import List

# Load .env from the root directory (one level up from backend/)
root_env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(root_env_path)

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For simplicity in dev, allowing all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = "openai/gpt-4o-mini"

# Initialize OpenRouter client
# OpenRouter uses the OpenAI SDK format
client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY", "dummy_key"),
)

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        if os.getenv("OPENROUTER_API_KEY") is None:
            return {"role": "assistant", "content": "Error: OPENROUTER_API_KEY is not set in backend/.env"}

        # Format messages for the API
        messages_formatted = [{"role": msg.role, "content": msg.content} for msg in request.messages]

        response = await client.chat.completions.create(
            model=request.model,
            messages=messages_formatted,
            # extra_headers={"HTTP-Referer": "http://localhost:5173", "X-Title": "LocalChat"}
        )
        
        return {"role": "assistant", "content": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("VITE_BACKEND_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
