import json
import re
import os
import requests
import paramiko

class Engine:
    def __init__(self, text, username, password, location):
        self.ssh = paramiko.SSHClient()
        self.username = username
        self.password = password
        self.location = location
        self.hostname = 'gw.info.unicaen.fr'
        self.text = text
        self.entities_images = None
        self.top_types = {
            'person': {'pattern': 'wordnet_person_', 'entities': {}},
            'organization': {'pattern': 'wordnet_organization_', 'entities': {}},
            'event': {'pattern': 'wordnet_event_', 'entities': {}},
            'artifact': {'pattern': 'wordnet_artifact_', 'entities': {}},
            'yagogeoentity': {'pattern': 'yagoGeoEntity', 'entities': {}}
        }

    def execute_AIDA(self):
        command = f'cd {self.location} && java -cp ".:./bin:./lib/*" mpi.aidalight.rmi.AIDALight_client "{self.text}"'
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.readlines()
        stdin.flush()
        self.ssh.close()
        return output[1:] if len(output) > 1 else None

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

