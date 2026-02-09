import re
from collections import Counter
import json
from typing import List, Dict, Tuple

from src.classes.my_sql_manager import MySqlManager


class Frequency:
    def __init__(self, mysql_manager: MySqlManager, top_words_count: int = 100):
        self.mysql_manager = mysql_manager
        self.top_words_count = top_words_count

    def _preprocess_text(self, text: str) -> List[str]:
        """Предварительная обработка текста: токенизация и очистка"""
        # Приведение к нижнему регистру и извлечение слов
        words = re.findall(r'\b[a-zA-Zа-яА-ЯёЁ]+\b', text.lower())
        return words

    def _calculate_word_frequencies(self, texts: List[str]) -> Dict[str, float]:
        """Вычисление частот слов из списка текстов"""
        all_words = []
        for text in texts:
            words = self._preprocess_text(text)
            all_words.extend(words)

        # Подсчет частот
        word_counts = Counter(all_words)
        total_words = len(all_words)

        # Преобразование в относительные частоты
        word_frequencies = {
            word: count / total_words
            for word, count in word_counts.most_common(self.top_words_count)
        }

        return word_frequencies

    def create_language_profiles(self):
        """Создание ПОЯ для русского и немецкого языков и сохранение в БД"""

        # Получение всех русских документов
        rus_documents = self.mysql_manager.get_all_rus_documents()
        rus_texts = [doc.text for doc in rus_documents]

        # Создание профиля для русского языка
        rus_profile = self._calculate_word_frequencies(rus_texts)

        # Сохранение профиля русского языка в БД
        self.mysql_manager.add_lang_search_image(
            language="russian",
            image=json.dumps(rus_profile, ensure_ascii=False)
        )

        # Получение всех немецких документов
        ger_documents = self.mysql_manager.get_all_ger_documents()
        ger_texts = [doc.text for doc in ger_documents]

        # Создание профиля для немецкого языка
        ger_profile = self._calculate_word_frequencies(ger_texts)

        # Сохранение профиля немецкого языка в БД
        self.mysql_manager.add_lang_search_image(
            language="german",
            image=json.dumps(ger_profile, ensure_ascii=False)
        )

        print("ПОЯ для русского и немецкого языков созданы и сохранены в БД")
        return {
            "russian": rus_profile,
            "german": ger_profile
        }

    def _create_document_profile(self, text: str) -> Dict[str, float]:
        """Создание ПОД (поискового образа документа) для входного текста"""
        words = self._preprocess_text(text)

        if not words:
            return {}

        # Подсчет частот слов в документе
        word_counts = Counter(words)
        total_words = len(words)

        # Преобразование в относительные частоты
        document_profile = {
            word: count / total_words
            for word, count in word_counts.items()
        }

        return document_profile

    def _calculate_similarity(self, doc_profile: Dict[str, float], lang_profile: Dict[str, float]) -> float:
        """Вычисление меры схожести между ПОД и ПОЯ"""
        similarity_score = 0.0

        for word, doc_frequency in doc_profile.items():
            if word in lang_profile:
                # Учитываем частоту слова в профиле языка
                lang_frequency = lang_profile[word]
                # Можно использовать различные метрики, например:
                # 1. Простое суммирование частот совпадающих слов
                similarity_score += lang_frequency
                # 2. Или произведение частот: similarity_score += doc_frequency * lang_frequency

        return similarity_score

    def detect_language(self, text: str) -> Tuple[str, Dict[str, float]]:
        """Определение языка текста методом частотных слов"""

        # Создание ПОД для входного текста
        document_profile = self._create_document_profile(text)

        if not document_profile:
            return "unknown", {}

        # Получение всех ПОЯ из базы данных
        lang_images = self.mysql_manager.get_all_lang_search_images()

        # Десериализация профилей и вычисление схожести
        language_scores = {}

        for lang_image in lang_images:
            try:
                lang_profile = json.loads(lang_image.image)
                similarity = self._calculate_similarity(document_profile, lang_profile)
                language_scores[lang_image.language] = similarity
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Ошибка при обработке профиля для {lang_image.language}: {e}")
                continue

        # Выбор языка с максимальной схожестью (только если есть ненулевые значения)
        if language_scores and max(language_scores.values()) > 0:
            detected_language = max(language_scores.items(), key=lambda x: x[1])[0]
        else:
            detected_language = "unknown"

        return detected_language, language_scores
