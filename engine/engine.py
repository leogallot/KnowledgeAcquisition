import requests
import re
import json


class Engine:
    def __init__(self):
        self.DBPEDIA_API_URL = "https://api.dbpedia-spotlight.org/en/annotate"
        self.AIDA_API_URL = "https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate"
        self.api = self.AIDA_API_URL
        self.toptypes = {
            'wordnet_person_': 'person',
            'wordnet_organization_': 'organization',
            'wordnet_event_': 'event',
            'wordnet_artifact': 'artifact',
            'yagoGeoEntity': 'yagogeoentity'
        }

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

    def get_top_type(self, entity_type):
        for top_type in self.toptypes:
            print('entity_type: ' + entity_type + ' | top type ' + top_type)
            print(entity_type in top_type)
            if top_type in entity_type:
                return self.toptypes[top_type]
        return None

    def get_representative_types(self, data):
        types = {}
        entities = data['entityMetadata']
        for value in entities.values():
            # check if value is not empty
            if value:
                entity = f'<{value["entityId"].lower()}>'
                entity_types = []
                top_type = None
                for entity_type in value['type']:
                    type_formatted = self.format_type(entity_type)
                    entity_types.append(type_formatted)
                    if top_type is None:
                        top_type = self.get_top_type(type_formatted)
                types[entity] = {'type': entity_types, 'toptype': top_type}

        return json.dumps(types)
