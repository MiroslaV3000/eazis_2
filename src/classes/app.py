import requests
from bs4 import BeautifulSoup
from src.classes.frequency import Frequency
from src.classes.alphabet import Alphabet
from src.classes.my_sql_manager import MySqlManager
from src.classes.neural_network import NeuralNetworkMethod
from src.classes.spider import Spider


class App:
    def __init__(self, mysql_manager: MySqlManager, frequency: Frequency, alphabet: Alphabet,
                 neural_network: NeuralNetworkMethod, spider: Spider):
        self.mysql_manager = mysql_manager
        self.frequency = frequency
        self.alphabet = alphabet
        self.neural_network = neural_network
        self.spider = spider

    def _parse(self):
        self.spider.parse_german(200)
        self.spider.parse_russian(200)

    def _create_language_profiles(self):
        self.frequency.create_language_profiles()

    @staticmethod
    def save_results_to_file(filename: str, results: dict):
        with open(f'var/{filename}.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(results, f, ensure_ascii=False, indent=2)
        return True

    def detect_language(self, url: str):
        site = requests.get(url)
        site_html = BeautifulSoup(site.content, 'html.parser')
        text = site_html.get_text()

        results = {
            'url': url  # Добавляем URL в результаты
        }

        detected_lang, scores = self.frequency.detect_language(text)
        results['frequency_method'] = {
            'language': detected_lang,
            'scores': scores
        }

        detected_lang, scores = self.alphabet.detect_language(text)
        results['alphabet_method'] = {
            'language': detected_lang,
            'scores': scores
        }

        detected_lang = self.neural_network.detect_language(text)
        results['neural_network_method'] = {
            'language': detected_lang,
            'scores': {detected_lang: 1}
        }
        return results


