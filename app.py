from flask import Flask, render_template, request
from engine.engine import Engine
from scraper.ScraperManager import ScraperManager
import json

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', data={'display': False})


@app.route('/endpoint/', methods=['GET', 'POST'])
def launch_engine():
    if request.method == 'POST' and check_request(request.json):

        url = request.json['url']
        username = request.json['username']
        password = request.json['password']
        location = request.json['location']
        text = ScraperManager().get_text_content(url)

        # if the scrap is too long
        if text is None:
            return json.dumps({'send': False, 'error': 'scrap'})

        engine = Engine(text=text, username=username, password=password, location=location)
        if engine.run():
            return json.dumps({'send': True, 'success': True})

        return json.dumps({'send': True, 'success': False})

    return json.dumps({'send': False, 'error': 'error'})


def check_request(data):
    for item in data:
        if data.get(item) == '':
            return False
    return True


if __name__ == '__main__':
    app.run()
