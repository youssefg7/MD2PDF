from langchain_openai.chat_models import ChatOpenAI
from functools import lru_cache

chatgpt = ChatOpenAI(
    model="gpt-4o-mini",
    stream_usage=True,
    streaming=True,
    temperature=0
)

@lru_cache()
def get_chatgpt():
    return chatgpt
