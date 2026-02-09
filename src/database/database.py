from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.testing.provision import drop_db

from src.database.config import DSN

# Создание движка базы данных
engine = create_engine(url=DSN)

# Создание сессии
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

