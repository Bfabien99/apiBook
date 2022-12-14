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


@app.route('/', methods=['GET','POST'])
def index():
    results = session.execute("SELECT * FROM authors").fetchall()
    data = [dict(row) for row in results]
    return jsonify(data)


@app.route('/authors', methods=['GET','POST'])
def getAuthors():
    results = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors ORDER BY fullname").fetchall()
    if results:
        data = [dict(row) for row in results]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))


@app.route('/authors/<id>', methods=['GET'])
def getAuthorsById(id):
    results = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors WHERE public_id = '{}'".format(id)).first()
    if results:
        data = [dict(results)]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))


@app.route('/authors/<id>/books', methods=['GET','POST'])
def getAuthorsBooks(id):
    author = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors WHERE public_id = '{}'".format(id)).first()
    if author:
        author = [dict(author)]
        results = session.execute("SELECT public_id AS id, title, description, cover, date, author_public_id AS author_id FROM books WHERE author_public_id = '{}' ORDER BY title".format(id)).fetchall()
        
        books = [dict(row) for row in results]
        
        data = dict(author=author, nb_books=len(books), books=books)
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))
    
    
    
    

@app.route('/books', methods=['GET','POST'])
def getBooks():
    results = session.execute("SELECT public_id AS id, title, description, cover, date, author_public_id AS author_id FROM books ORDER BY title").fetchall()
    data = [dict(row) for row in results]
    if results:
        data = [dict(row) for row in results]
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))


@app.route('/books/<id>', methods=['GET'])
def getBooksById(id):
    results = session.execute("SELECT public_id AS id, title, description, cover, date, author_public_id AS author_id FROM books WHERE public_id = '{}'".format(id)).first()
    if results:
        book = [dict(results)]
        author_id = book[0]["author_id"]
        
        author = session.execute("SELECT public_id AS id, fullname, birth, bio FROM authors WHERE public_id = '{}'".format(author_id)).first()
        author = [dict(author)]
        
        data = dict(author=author, books=book)
        return jsonSend(200, "data found", data)
    return jsonify(dict(message="no data found",results=[]))





### Generate Fake Data ###
@app.route('/fakeData/book/<int:number>', methods=['GET','POST'])
def fakeBook(number):
    
    results = session.execute("SELECT public_id, fullname, birth, bio FROM authors").fetchall()
    
    data = [dict(row) for row in results]
        
    for i in range(number):
        r = int(random.randrange(0, len(data)))
        session.add(Books(public_id=f"{faker.uuid4()}", title=f"{faker.text(max_nb_chars=50)}", description=f"{faker.sentence()}", cover=f"{faker.image_url()}", date=f"{faker.date_of_birth()}", author_public_id=f"{data[r]['public_id']}"))
        session.commit()
    
    return jsonify(dict(data="ok"))

@app.route('/fakeData/author/<int:number>', methods=['GET','POST'])
def fakeAuthor(number):
    for i in range(number):
        session.add(Authors(public_id=f"{faker.uuid4()}", fullname=f"{faker.name()}", birth=f"{faker.date_of_birth()}", bio=f"{faker.text()}"))
        session.commit()
    
    return jsonify(dict(data="ok"))

if __name__ == '__main__':
    session.rollback()
    app.run(debug=True)