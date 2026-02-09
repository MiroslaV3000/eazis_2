import requests
from bs4 import BeautifulSoup
import re

from src.classes.my_sql_manager import MySqlManager



class Spider:

    def __init__(self, my_sql_manager: MySqlManager):
        self.my_sql_manager = my_sql_manager
        self.german_site_url = 'https://www.kochbar.de/rezepte/alle-rezepte.html'
        self.russian_site_url = 'https://www.gastronom.ru/group/recepty-supov-1129'

    @staticmethod
    def clean_recipe_text(text: str) -> str:
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\säöüÄÖÜß.,!?;:-]', '', text)
        text = text.strip()
        sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
        cleaned_text = '. '.join(sentences)
        return cleaned_text



    def parse_german(self, recipe_limit: str = None):
        page_number = 1
        recipe_number = 1

        while True:
            site = requests.get(self.german_site_url + f'?sort=create&order=desc&page={page_number}')
            site_html = BeautifulSoup(site.content, 'html.parser')
            recipes = site_html.select('.kb-teaser-list-link')


            if len(recipes):
                for recipe in recipes:
                    if recipe_limit is None or recipe_number <= recipe_limit:
                        recipe_url = recipe.get('href')
                        recipe_site = requests.get(recipe_url)
                        recipe_site_html = BeautifulSoup(recipe_site.content, 'html.parser')

                        recipe_title = recipe_site_html.select('.recipe-head-headline')[0].text
                        recipe_text = recipe_site_html.get_text()
                        clean_recipe_text = Spider.clean_recipe_text(recipe_text)
                        print(recipe_title, clean_recipe_text, recipe_url)
                        self.my_sql_manager.add_ger_document(title=recipe_title, url=recipe_url, text=clean_recipe_text)
                        recipe_number +=1
                    else:
                        return 0

                page_number += 1
            else:
                return 0

    def parse_russian(self, recipe_limit: str = None):
        page_number = 1
        recipe_number = 1

        while True:
            site = requests.get(self.russian_site_url + f'?page={page_number}')
            site_html = BeautifulSoup(site.content, 'html.parser')
            recipes = site_html.select('._name_7i4i1_18')


            if len(recipes):
                for recipe in recipes:
                    if recipe_limit is None or recipe_number <= recipe_limit:
                        recipe_url = 'https://www.gastronom.ru' + recipe.get('href')
                        recipe_site = requests.get(recipe_url)
                        recipe_site_html = BeautifulSoup(recipe_site.content, 'html.parser')

                        recipe_title = recipe_site_html.select('.materialTitle')[0].text
                        recipe_text = recipe_site_html.get_text()
                        clean_recipe_text = Spider.clean_recipe_text(recipe_text)
                        print(recipe_title, clean_recipe_text, recipe_url)
                        self.my_sql_manager.add_rus_document(title=recipe_title, url=recipe_url, text=clean_recipe_text)
                        recipe_number +=1
                    else:
                        return 0

                page_number += 1
            else:
                return 0



























    
