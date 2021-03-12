from flask import Flask, render_template, request

from engine.engine import Engine
from engine.database import Database
from scraper.ScraperManager import ScraperManager

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and check_request(request.form):

        url = request.form.get('url')
        username = request.form.get('username')
        password = request.form.get('password')
        location = request.form.get('location')

        text = ScraperManager().get_text_content(url)
        # if the scrap is too long
        if text is None:
            # TODO update the output
            return 'Too long'

        engine = Engine(text, username, password, location)
        temp = engine.execute_AIDA()
        '''
        url = request.form.get('url')
        text = ScraperManager().get_text_content(url)

        if text is None:
            return 'Too long'

        engine = Engine(text)
        engine.disambiguate()
        engine.extract_entities_types()
        engine.save_entities_types()
        engine.find_representative_entities_types()
        engine.extract_entities_images()
        
        output = {'display': True, 'article': text, 'url': url, 'images': engine.get_entities_images()}
        return render_template('index.html', data=output)
        '''
        return 'OK'
    return render_template('index.html', data={'display': False})


def check_request(data):
    for item in data:
        if data.get(item) == '':
            return False
    return True


if __name__ == '__main__':
    app.run()
