from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class GermanDocumentOrm(Base):
    __tablename__ = "german_document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(400))
    url: Mapped[str] = mapped_column(String(400))
    text: Mapped[str] = mapped_column(Text)

class RussianDocumentOrm(Base):
    __tablename__ = "russian_document"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(400))
    url: Mapped[str] = mapped_column(String(400))
    text: Mapped[str] = mapped_column(Text)

class LangSearchImageOrm(Base):
    __tablename__ = "lang_search_image"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    language: Mapped[str] = mapped_column(String(400))
    image: Mapped[str] = mapped_column(Text)

