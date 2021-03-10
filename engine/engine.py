import requests
import re
import json


class Engine:
    def __init__(self):
        self.DBPEDIA_API_URL = "https://api.dbpedia-spotlight.org/en/annotate"
        self.AIDA_API_URL = "https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate"
        self.api = self.AIDA_API_URL

    def disambiguate(self, text):
        response = requests.post(self.api, {'text': text})
        return response.json()

    def get_entities_images(self, data):
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

    def format_type(self, entity_type):
        return entity_type.replace('YAGO_', '<') + '>'

    def get_representative_types(self, data):
        types = {}
        entities = data['entityMetadata']
        for value in entities.values():
            if value:
                entity = f'<{value["entityId"].lower()}>'
                entity_types = list(map(self.format_type, set(value['type'])))
                types[entity] = entity_types
        return json.dumps(types)
