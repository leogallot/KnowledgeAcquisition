import requests
import re

DBPEDIA_API_URL = "https://api.dbpedia-spotlight.org/en/annotate"
AIDA_API_URL = "https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate"


def disambiguate(text, confidence=0.5):
    response = requests.post(AIDA_API_URL, {'text': text})
    return response.json()


def get_entities_images(data):
    items = []
    images = []

    for item in data['entityMetadata']:
        if re.search('YAGO:', item):
            items.append(item)

    for item in items:
        url = data['entityMetadata'][item]['depictionurl']
        if url is not None:
            images.append(url)

    return images
