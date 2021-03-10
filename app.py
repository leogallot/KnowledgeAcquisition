from flask import Flask, render_template, request

from engine.engine import Engine
from scraper.ScraperManager import ScraperManager

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('url') != '':
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
    return render_template('index.html', data={'display': False})


if __name__ == '__main__':
    app.run()
