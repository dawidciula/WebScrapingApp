from flask import Flask, render_template
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    url = "https://www.skapiec.pl"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return render_template('index.html', content=soup.prettify())


if __name__ == '__main__':
    app.run()
