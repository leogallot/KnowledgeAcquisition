from flask import Flask, render_template, request

from scraper.ScraperManager import ScraperManager

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.form.get('url') != '':
        article = ScraperManager(request.form.get('url')).get_text()
        output = {'display': True, 'article': article, 'url': request.form.get('url')}
        return render_template('index.html', data=output)
    return render_template('index.html', data={'display': False})


if __name__ == '__main__':
    app.run()
