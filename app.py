from flask import Flask, render_template, request

from engine.engine import *
from scraper.ScraperManager import ScraperManager

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('url') != '':
        url = request.form.get('url')

        article = ScraperManager(url).get_text()
        entities_data = disambiguate(article)

        types = get_representative_types(entities_data)
        images = get_entities_images(entities_data)

        output = {'display': True, 'article': article, 'url': url, 'images': images}
        return render_template('index.html', data=output)
    return render_template('index.html', data={'display': False})


if __name__ == '__main__':
    app.run()
