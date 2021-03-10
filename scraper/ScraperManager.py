from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
import requests


class ScraperManager:

    def get_text_content(self, url):
        queue = Queue()
        process = Process(target=self.get_text, args=(url, queue,))
        process.start()
        try:
            res = queue.get(timeout=15)
            process.join()
            return res
        except:
            process.terminate()
            return None

    def get_text(self, url, queue):
        article = requests.get(url)
        soup = BeautifulSoup(article.content, 'html.parser')
        body = soup.find('body')
        queue.put(''.join([p.text for p in body.findAll('p')]))
