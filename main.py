from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}

@app.post("/generate")
async def generate(req: Request):
    try:
        data = await req.json()
        prompt = data["prompt"]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        start = answer.find("[")
        end = answer.rfind("]") + 1
        clean_answer = answer[start:end]

        return {"object": clean_answer}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}