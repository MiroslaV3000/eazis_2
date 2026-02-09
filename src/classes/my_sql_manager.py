from sqlalchemy import select
from src.database.database import Base
from src.database.models import RussianDocumentOrm, GermanDocumentOrm, LangSearchImageOrm


class MySqlManager:
    def __init__(self, engine, session_factory):
        self.engine = engine
        self.session_factory = session_factory
        # self.create_tables()


    def create_tables(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    #Russian
    def add_rus_document(self, title: str, url: str, text: str) -> RussianDocumentOrm:
        with self.session_factory() as session:
            document = RussianDocumentOrm(title=title, url=url, text=text)
            session.add(document)
            session.commit()
            session.refresh(document)
            return document


    def get_rus_document_by_id(self, document_id: int) -> RussianDocumentOrm:
        with self.session_factory() as session:
            query = (
                select(
                    RussianDocumentOrm
                )
                .select_from(
                    RussianDocumentOrm
                )
                .where(RussianDocumentOrm.id == document_id)
            )
            document = session.execute(query)
            return document.scalars().first()


    def get_all_rus_documents(self) -> list[RussianDocumentOrm]:
        with self.session_factory() as session:
            query = (
                select(
                    RussianDocumentOrm
                )
                .select_from(
                    RussianDocumentOrm
                )
            )
            documents = session.execute(query)
            return documents.scalars().all()


    #German
    def add_ger_document(self, title: str, url: str, text: str) -> GermanDocumentOrm:
        with self.session_factory() as session:
            document = GermanDocumentOrm(title=title, url=url, text=text)
            session.add(document)
            session.commit()
            session.refresh(document)
            return document


    def get_ger_document_by_id(self, document_id: int) -> GermanDocumentOrm:
        with self.session_factory() as session:
            query = (
                select(
                    GermanDocumentOrm
                )
                .select_from(
                    GermanDocumentOrm
                )
                .where(GermanDocumentOrm.id == document_id)
            )
            document = session.execute(query)
            return document.scalars().first()


    def get_all_ger_documents(self) -> list[GermanDocumentOrm]:
        with self.session_factory() as session:
            query = (
                select(
                    GermanDocumentOrm
                )
                .select_from(
                    GermanDocumentOrm
                )
            )
            documents = session.execute(query)
            return documents.scalars().all()


    # LangSearchImage methods
    def add_lang_search_image(self, language: str, image: str) -> LangSearchImageOrm:
        with self.session_factory() as session:
            lang_search_image = LangSearchImageOrm(language=language, image=image)
            session.add(lang_search_image)
            session.commit()
            session.refresh(lang_search_image)
            return lang_search_image

    def get_all_lang_search_images(self) -> list[LangSearchImageOrm]:
        with self.session_factory() as session:
            query = select(LangSearchImageOrm)
            result = session.execute(query)
            return result.scalars().all()