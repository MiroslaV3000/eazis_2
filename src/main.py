from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import main_router

server = FastAPI()
server.include_router(main_router)

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники (для тестирования)
    allow_credentials=True,  # Разрешаем отправку cookies
    allow_methods=["*"],  # Разрешаем все HTTP-методы
    allow_headers=["*"]  # Разрешаем все заголовки
)