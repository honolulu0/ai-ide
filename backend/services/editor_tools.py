from .llm_client import chat_with_llm
from ..models import InlineEditRequest, ChatMessage

INLINE_SYSTEM_PROMPT = """
你是一个专业的代码重构助手。
你只返回修改后的代码，不要额外解釋，不要包裹```代码块。
"""

async def inline_edit(req: InlineEditRequest) -> str:
    user_prompt = (
        f"语言: {req.language or 'unknown'}\n"
        f"用户指令: {req.instruction}\n"
        f"下面是原始代码，请根据指令进行修改，只返回修改后的完整代码：\n\n"
        f"{req.original_code}"
    )

    messages = [
        ChatMessage(role="system", content=INLINE_SYSTEM_PROMPT),
        ChatMessage(role="user", content=user_prompt),
    ]

    result = await chat_with_llm(messages)
    return result
