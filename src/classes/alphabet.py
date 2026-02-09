import re
from typing import Tuple, Dict


class Alphabet:
    def __init__(self):
        # Заранее известные алфавиты
        self.russian_alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        self.german_alphabet = set('abcdefghijklmnopqrstuvwxyzäöüß')

    def detect_language(self, text: str) -> Tuple[str, Dict[str, float]]:
        """Определение языка по проценту совпадения букв с алфавитами"""

        # Извлекаем все буквы из текста
        letters = re.findall(r'[a-zA-Zа-яА-ЯёЁäöüß]', text.lower())

        if not letters:
            return "unknown", {'russian': 0.0, 'german': 0.0}

        # Считаем процент букв, которые есть в каждом алфавите
        russian_count = sum(1 for char in letters if char in self.russian_alphabet)
        german_count = sum(1 for char in letters if char in self.german_alphabet)

        russian_percent = russian_count / len(letters)
        german_percent = german_count / len(letters)

        scores = {
            'russian': russian_percent,
            'german': german_percent
        }

        # Выбираем язык с наибольшим процентом
        if russian_percent > german_percent:
            detected_language = "russian"
        elif german_percent > russian_percent:
            detected_language = "german"
        else:
            detected_language = "unknown"
        print(scores)
        return detected_language, scores