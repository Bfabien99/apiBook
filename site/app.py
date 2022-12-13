from flask import Flask, request, redirect, render_template, url_for
import urllib.request, json


app = Flask(__name__)


def callAPI(endpoint):
    url = "http://localhost:5000/{}".format(endpoint)

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    
    return dict['results']


@app.route('/')
@app.route('/index')
def home_page():
    books = callAPI("books")
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)