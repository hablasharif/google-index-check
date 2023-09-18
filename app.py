import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

def check_indexed(url):
    google = "https://www.google.com/search?q=site:" + url + "&hl=en"
    response = requests.get(google, cookies={"CONSENT": "YES+1"})
    soup = BeautifulSoup(response.content, "html.parser")
    not_indexed = re.compile("did not match any documents")

    if soup(text=not_indexed):
        return f"The page '{url}' is NOT indexed by Google."
    else:
        return f"The page '{url}' is indexed by Google."

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        urls = request.form['urls'].split()
        results = [check_indexed(url) for url in urls]
        result = '\n'.join(results)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
