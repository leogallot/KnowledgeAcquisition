import json
import re
import os
import requests
import paramiko
from engine.database import Database


class Engine:
    def __init__(self, text, username, password, location):
        self.ssh = paramiko.SSHClient()
        self.db = Database(dbname='yago', username='postgres', password='password', host='127.0.0.1')
        self.username = username
        self.password = password
        self.location = location
        self.hostname = 'gw.info.unicaen.fr'
        self.text = text
        self.entities_images = None
        self.entities = []
        self.pattern_top_types = {
            'person': '<wordnet_person_',
            'organization': '<wordnet_organization_',
            'event': '<wordnet_event_',
            'artifact': '<wordnet_artifact_',
            'yagogeoentity': '<yagoGeoEntity>'
        }
        self.top_types = {
            'person': {'pattern': 'wordnet_person_', 'entities': {}},
            'organization': {'pattern': 'wordnet_organization_', 'entities': {}},
            'event': {'pattern': 'wordnet_event_', 'entities': {}},
            'artifact': {'pattern': 'wordnet_artifact_', 'entities': {}},
            'yagogeoentity': {'pattern': 'yagoGeoEntity', 'entities': {}}
        }

    # Execute AIDA on distant server
    def execute_AIDA(self):
        command = f'cd {self.location} && java -cp ".:./bin:./lib/*" mpi.aidalight.rmi.AIDALight_client "{self.text}"'
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.readlines()
        stdin.flush()
        self.ssh.close()
        self.clean_output_AIDA(output[1:])
        self.execute_YAGO()

        print(self.entities)

        return output[1:] if len(output) > 1 else None

    # Clean AIDA output
    def clean_output_AIDA(self, output_aida):
        for index in range(0, len(output_aida)):
            output_split = output_aida[index].split('\t')  # split the output (\t)
            word = output_split[0]  # get the name of entity
            entity = output_split[1].split('/')  # split the wikipedia URL
            entity = f'<{entity[len(entity) - 1][:-1]}>'  # get the end of URL
            if entity != '<--NME-->':
                if not any(ent['word'] == word for ent in self.entities):   # check there isn't same word
                    self.entities.append({'word': word, 'entity': entity})

    # Get YAGO from database
    def execute_YAGO(self):
        for index in range(0, len(self.entities)):
            temporary_result = self.db.execute(self.entities[index]['entity'])
            self.entities[index]['yago'] = []
            for i in range(0, len(temporary_result)):
                if re.match('<wordnet_', temporary_result[i][0]) or re.match('<yagoGeoEntity>', temporary_result[i][0]):
                    self.entities[index]['yago'].append(temporary_result[i][0])

    # Prepare data for PURE framework
    def prepare_PURE(self):
        for index in range(0, len(self.entities)):
            top_type = None
            for yago_type in self.entities[index]['yago']:
                if top_type is None:
                    top_type = self.find_top_type(yago_type)
                    # not terminated

    # Execute PURE framework
    def execute_PURE(self):
        pass

    def disambiguate(self):
        response = requests.post(self.api, {'text': self.text})
        self.api_response = response.json()

    def extract_entities_images(self):
        items = []
        images = []

        for item in self.api_response['entityMetadata']:
            if re.search('YAGO:', item):
                items.append(item)

        for item in items:
            url = self.api_response['entityMetadata'][item]['depictionurl']
            if url is not None:
                images.append(url)

        self.entities_images = images

    def get_entities_images(self):
        return self.entities_images

    def format_entity_type(self, entity_type):
        return entity_type.replace('YAGO_', '<') + '>'

    def find_top_type(self, entity_type):
        for top_type in self.top_types:
            if self.top_types[top_type]['pattern'] in entity_type:
                return top_type
        return None

    def extract_entities_types(self):
        entities = self.api_response['entityMetadata']
        for value in entities.values():
            # check if value is not empty
            if value:
                entity = f'<{value["entityId"].lower()}>'
                entity_types = []
                top_type = None
                for entity_type in value['type']:
                    type_formatted = self.format_entity_type(entity_type)
                    entity_types.append(type_formatted)
                    if top_type is None:
                        top_type = self.find_top_type(type_formatted)
                if top_type in self.top_types:
                    self.top_types[top_type]['entities'][entity] = entity_types

    def save_entities_types(self):
        for top_type in self.top_types:
            with open(f'tmp/{top_type}.json', 'w+') as file:
                json.dump(self.top_types[top_type]['entities'], file)

    def find_representative_entities_types(self):
        for top_type in self.top_types:
            command = f'python3 -W ignore PURE/run.py {top_type} ../tmp/{top_type}.json 100 > tmp/pure_{top_type}.txt'
            os.system(command)
