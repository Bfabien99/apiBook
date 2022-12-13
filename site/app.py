from flask import Flask, request, redirect, render_template, url_for
import urllib.request, json
import random


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
    nb_book = len(books)
    random.shuffle(books)
    del books[15:]
    
    authors = callAPI("authors")
    nb_author = len(authors)
    random.shuffle(authors)
    del authors[15:]
    
    return render_template('index.html', books=books, nb_book=nb_book, authors=authors, nb_author=nb_author)


@app.route('/books')
def books_page():
    books = callAPI("books")
    nb_book = len(books)
    
    return render_template('books.html', books=books, nb_book=nb_book,)

@app.route('/books/<string:id>')
def showbook_page(id):
    results = callAPI("books/{}".format(id))
    books=author={}
    if results:
        author = results['author']
        books = results['books']
    return render_template('showbook.html', books=books, author=author)


@app.route('/authors')
def authors_page():
    authors = callAPI("authors")
    nb_author = len(authors)
    return render_template('authors.html', authors=authors, nb_author=nb_author)

@app.route('/authors/<string:id>')
def showauthor_page(id):
    books = author = {}
    results = callAPI("authors/{}/books".format(id))
    if results:
        author = results['author']
        books = results['books']
    return render_template('showauthor.html', authors=author, books=books)

if __name__ == '__main__':
    app.run(debug=True)