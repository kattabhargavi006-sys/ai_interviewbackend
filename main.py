from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(data: PromptRequest):
    return {
        "response": f"Generated content for: {data.prompt}"
    }