from typing import List
from openai import OpenAI
from ..config import settings
from ..models import ChatMessage

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)

async def chat_with_llm(messages: List[ChatMessage]) -> str:
    # Convert to OpenAI message format
    openai_msgs = [{"role": m.role, "content": m.content} for m in messages]

    resp = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=openai_msgs,
        temperature=0.2,
    )
    return resp.choices[0].message.content


async def complete_code(prompt: str) -> str:
    resp = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content
