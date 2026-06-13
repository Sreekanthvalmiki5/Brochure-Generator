"""
Brochure Generator Backend — FastAPI
Drop-in replacement for the Gradio-based Day2 class.

Install:
    pip install fastapi uvicorn httpx python-dotenv openai beautifulsoup4 requests

Run:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

Deploy:
    - Railway / Render / Fly.io: just point to this file
    - Docker:  see Dockerfile below
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal
import asyncio
import os

# ---------------------------------------------------------------------------
# Optional: load .env for local dev
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from openai import OpenAI          # openrouter uses the openai SDK
from backend.completions.scrapper import fetch_website_contents   # your existing scrapper module

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(title="Brochure Generator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# OpenRouter client  (reuse your existing models.py logic or inline here)
# ---------------------------------------------------------------------------
def get_client() -> OpenAI:
    api_key = os.getenv("OPEN_ROUTER_API_KEY", "")
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

MODEL_MAP: dict[str, str] = {
    "CHATGPT":  "gpt-oss-20b",
    "GEMMA":    "gemma-4-26b-a4b-it",
    "META":     "llama-3.2-3b-instruct",
    "LIQUID":   "liquid/lfm-2.5-1.2b-instruct",
    "NEX":      "nex-n2-pro",
    "HERMES":   "hermes-3-llama-3.1-405b",
    "QWEN":     "qwen3-coder",
    "VENICE":   "dolphin-mistral-24b-venice-edition",
}

SYSTEM_MESSAGE = (
    "You are an assistant that analyzes the contents of a company website "
    "landing page and creates a short brochure about the company for "
    "prospective customers, investors and recruits. "
    "Respond in markdown without code blocks."
)

# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------
class BrochureRequest(BaseModel):
    company_name: str
    url: str
    model: Literal["CHATGPT", "GEMMA", "META", "LIQUID", "NEX", "HERMES", "QWEN", "VENICE"] = "CHATGPT"

# ---------------------------------------------------------------------------
# Streaming endpoint
# ---------------------------------------------------------------------------
@app.post("/generate-brochure")
async def generate_brochure(req: BrochureRequest):
    model_id = MODEL_MAP.get(req.model)
    if not model_id:
        raise HTTPException(status_code=400, detail=f"Unknown model: {req.model}")

    # Fetch the landing page (runs in thread to avoid blocking the event loop)
    try:
        page_content = await asyncio.to_thread(fetch_website_contents, req.url)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not fetch URL: {e}")

    prompt = (
        f"Generate a brochure for {req.company_name}. "
        f"Here is the landing page of the company:\n\n{page_content}"
    )

    async def token_stream():
        client = get_client()
        try:
            stream = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user",   "content": prompt},
                ],
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    # SSE format: "data: <text>\n\n"
                    yield f"{token}"
            # yield "data: [DONE]\n\n"  
        except Exception as e:
            yield f"data: ERROR: {e}\n\n"

    return StreamingResponse(
        token_stream(),
          media_type="text/plain",
        # media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # important for nginx proxies
        },
    )

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)