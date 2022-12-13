from flask import Flask, request, jsonify

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import random

from faker import Faker


app = Flask(__name__)

### set database parameters with sqlalchemy ###
Base = automap_base()

# engine, suppose it has two tables 'authors' and 'books' set up
engine = create_engine("mysql+pymysql://root:@localhost:3306/apibooks")

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
Authors = Base.classes.authors
Books = Base.classes.books

session = Session(engine)
### ###
### init faker ###
faker = Faker()
### ###

def jsonSend(code:int, message:str, results={}):
    return jsonify(dict(message=message,results=results)), code


@app.route('/')
def index():
    results = session.execute("SELECT * FROM authors").fetchall()
    data = [dict(row) for row in results]
    return jsonify(data)


@app.route('/authors')
def getAuthors():
    results = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors").fetchall()
    if results:
        data = [dict(row) for row in results]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))


@app.route('/authors/<id>')
def getAuthorsById(id):
    results = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors WHERE public_id = '{}'".format(id)).first()
    if results:
        data = [dict(results)]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))


@app.route('/authors/<id>/books')
def getAuthorsBooks(id):
    author = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors WHERE public_id = '{}'".format(id)).first()
    if author:
        author = [dict(author)]
        results = session.execute("SELECT public_id AS id, title, description, cover, date, author_public_id AS author_id FROM books WHERE author_public_id = '{}'".format(id)).fetchall()
        
        books = [dict(row) for row in results]
        
        data = [dict(author=author, nb_books=len(books), books=books)]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))
    
    
    
    

@app.route('/books')
def getBooks():
    results = session.execute("SELECT public_id AS id, title, description, cover, date, author_public_id AS author_id FROM books").fetchall()
    data = [dict(row) for row in results]
    if results:
        data = [dict(row) for row in results]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))


@app.route('/books/<id>')
def getBooksById(id):
    results = session.execute("SELECT public_id AS id, title, description, cover, date, author_public_id AS author_id FROM books WHERE public_id = '{}'".format(id)).first()
    if results:
        data = [dict(results)]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))





### Generate Fake Data ###
@app.route('/fakeData/book/<int:number>')
def fakeBook(number):
    
    results = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors").fetchall()
    
    data = [dict(row) for row in results]
        
    for i in range(number):
        r = int(random.randrange(0, len(data)))
        session.add(Books(public_id=f"{faker.uuid4()}", title=f"{faker.name()}", description=f"{faker.sentence()}", cover=f"{faker.image_url()}", date=f"{faker.date_of_birth()}", author_public_id=f"{data[r]['public_id']}"))
        session.commit()
    
    return jsonify(dict(data="ok"))

@app.route('/fakeData/author/<int:number>')
def fakeAuthor(number):
    for i in range(number):
        session.add(Authors(public_id=f"{faker.uuid4()}", fullname=f"{faker.name()}", birth=f"{faker.date_of_birth()}", bio=f"{faker.text()}"))
        session.commit()
    
    return jsonify(dict(data="ok"))

if __name__ == '__main__':
    app.run(debug=True)