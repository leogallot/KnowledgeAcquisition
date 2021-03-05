from bs4 import BeautifulSoup
import requests


class ScraperManager:

    def __init__(self, url):
        self.article = requests.get(url)
        self.soup = BeautifulSoup(self.article.content, 'html.parser')
        self.body = self.get_text()

    def get_text(self):
        body = self.soup.find('body')
        return [p.text for p in body.findAll('p')]
