import json
import re
import os
import hashlib
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
        self.entities = []
        self.top_types = {
            'person': {'pattern': 'wordnet_person_', 'entities': {}},
            'organization': {'pattern': 'wordnet_organization_', 'entities': {}},
            'event': {'pattern': 'wordnet_event_', 'entities': {}},
            'artifact': {'pattern': 'wordnet_artifact_', 'entities': {}},
            'yagogeoentity': {'pattern': 'yagoGeoEntity', 'entities': {}}
        }
        self.wikipedia = [] # contains {'word': str, 'wikipedia_id': str}

    # Run engine
    def run(self):
        print('-- EXECUTING AIDA (SSH SERVER)')
        aida_output = self.execute_AIDA()

        if aida_output is not None:
            print('-- CLEANING AIDA OUTPUT')
            self.clean_output_AIDA(aida_output)

            print('-- FINDING ENTITIES IN YAGO DATABASE')
            self.execute_YAGO()

            print('-- CLEANING DATA TO USE PURE FRAMEWORK')
            self.prepare_top_type_PURE()
            self.save_entities_types()

            print('-- EXECUTING PURE')
            # self.execute_PURE()

            print('-- GET PURE OUTPUT')
            # pure = self.read_pure_files()

            print('-- CREATE WIKIPEDIA ITEMS')
            text = self.process_text_wikipedia()

            print('-- END')
            return {'text': text, 'pure': 'pure'}

        return None

    # Execute AIDA on distant server
    def execute_AIDA(self):
        command = f'cd {self.location} && java -cp ".:./bin:./lib/*" mpi.aidalight.rmi.AIDALight_client "{self.text}"'
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.readlines()
        stdin.flush()
        self.ssh.close()

        return output[1:] if len(output) > 1 else None

    # Clean AIDA output
    def clean_output_AIDA(self, output_aida):
        for index in range(0, len(output_aida)):
            output_split = output_aida[index].split('\t')  # split the output (\t)
            word = output_split[0]  # get the name of entity
            entity = output_split[1].split('/')  # split the wikipedia URL
            entity = entity[len(entity) - 1][:-1]
            self.wikipedia.append({'word': word, 'wikipedia_id': output_split[1][:-1]})
            entity = f'<{entity}>'  # get the end of URL
            if entity != '<--NME-->':
                if not any(ent['word'] == word for ent in self.entities):  # check there isn't same word
                    self.entities.append({'word': word, 'entity': entity})

    # Get YAGO from database
    def execute_YAGO(self):
        for index in range(0, len(self.entities)):
            temporary_result = self.db.execute(self.entities[index]['entity'])
            self.entities[index]['yago'] = []
            for i in range(0, len(temporary_result)):
                if re.match('<wordnet_', temporary_result[i][0]) or re.match('<yagoGeoEntity>', temporary_result[i][0]):
                    self.entities[index]['yago'].append(temporary_result[i][0])

    # Prepare top type for PURE framework
    def prepare_top_type_PURE(self):
        for index in range(0, len(self.entities)):
            top_type = None
            self.entities[index]['top-type'] = ''  # add to entities the top type (maybe not utils)
            for yago_type in self.entities[index]['yago']:
                if top_type is None:
                    top_type = self.find_top_type(yago_type)  # find top type
            if top_type is not None and top_type in self.top_types:
                # add to top_types the entity
                self.top_types[top_type]['entities'][self.entities[index]['word']] = self.entities[index]['yago']
            self.entities[index]['top-type'] = top_type

    # Save entities in files
    def save_entities_types(self):
        for top_type in self.top_types:
            with open(f'tmp/{top_type}.json', 'w+') as file:
                json.dump(self.top_types[top_type]['entities'], file)

    # Execute PURE framework
    def execute_PURE(self):
        for top_type in self.top_types:
            command = f'python3 -W ignore PURE/run.py {top_type} ../tmp/{top_type}.json 100 > tmp/pure_{top_type}.txt'
            os.system(command)

    # Read PURE files
    def read_pure_files(self):
        content = []
        for index, top_type in enumerate(self.top_types):
            file = open(f'tmp/pure_{top_type}.txt', 'r')
            lines = file.readlines()
            content.append({'top': top_type, 'content': []})
            for line in lines[1:]:
                temp = line.split('>')  # split line type : <wordnet_XXXX_YYYY>ZZ.ZZ where ZZ.ZZ is PURE result
                wordnet = temp[0]+'>'
                score = float(temp[1])
                if score > 0:
                    for entity in self.top_types[top_type]['entities']:
                        if any(wordnet in entity_type for entity_type in self.top_types[top_type]['entities'][entity]):
                            content[index]['content'].append({'entity': entity, 'wordnet': wordnet, 'score': round(score, 2)})
        return content

    def process_text_wikipedia(self):
        text_clean = []
        text_split = self.text.split(' ') # split text with space
        for word in text_split:
            if any(wiki['word'] == word for wiki in self.wikipedia):
                text_clean.append({'mark': True, 'word': word, 'link': self.get_wikipedia_link(word)})
            else:
                text_clean.append({'mark': False, 'word': word})
        return text_clean

    # Get wikipedia link
    def get_wikipedia_link(self, word):
        wikipedia_img = ''
        # get the good wikipedia ID
        for item in self.wikipedia:
            if item['word'] == word:
                wikipedia_img = item['wikipedia_id']
                break
        return wikipedia_img

    # Get top type of entity
    def find_top_type(self, entity_type):
        for top_type in self.top_types:
            if self.top_types[top_type]['pattern'] in entity_type:
                return top_type
        return None
