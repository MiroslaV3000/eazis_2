from typing import Optional
from pydantic import BaseModel



class LoadTelegramChatsScheme(BaseModel):
    user_id: int


class TelegramChatResponse(BaseModel):
    id: int
    user_id: int
    chat_id: int
    chat_name: str
    chat_icon: Optional[str] = None

class AddTelegramContextScheme(BaseModel):
    user_id: int
    llm_chat_id: int
    messages: list[str]


class AddTelegramFileContextScheme(BaseModel):
    user_id: int
    llm_chat_id: int
    tg_chat_id: int
    file_id: int




