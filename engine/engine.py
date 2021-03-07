import requests

DBPEDIA_API_URL = "https://api.dbpedia-spotlight.org/en/annotate"


def disambiguate(text, confidence=0.5):
    response = requests.post(DBPEDIA_API_URL, {'text': text, 'confidence': confidence})
    data = response.json()
    entities = [resource for resource in data['Resources'][:5]]
    return {'entities': entities, 'confidence': confidence}
