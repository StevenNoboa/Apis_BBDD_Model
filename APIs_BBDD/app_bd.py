import json
from flask import Flask, request, jsonify
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

# 0.Ruta para obtener todos los libros
@app.route('/v0/books', methods=['GET'])
def all_books():
    connection = sqlite3.connect("books.db")
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM books;")
    books_data = crsr.fetchall()
   
    return jsonify(books_data)

# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/v0/books_author', methods=['GET'])
def all_books_author():
    connection = sqlite3.connect("books.db")
    crsr = connection.cursor()
    crsr.execute('''
        SELECT author, COUNT(*) as book_count
        FROM books
        GROUP BY author
        ORDER BY book_count DESC;
                 ''')
    books_author = crsr.fetchall()
   
    return jsonify(books_author)

# 2.Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/v0/author', methods=['GET'])
def author_books():
    connection = sqlite3.connect("books.db")
    crsr = connection.cursor()
    author = request.args['author']
    crsr.execute('''
        SELECT *
        FROM books
        WHERE author = ?;
    ''', (author,))
    author_books = crsr.fetchall()
   
    return jsonify(author_books)

# 3.Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/v0/params', methods=['GET'])
def books_params():
    connection = sqlite3.connect("books.db")
    crsr = connection.cursor()
    title = request.args['title']
    published = request.args['published']
    author = request.args['author']
    crsr.execute('''
        SELECT *
        FROM books
        WHERE title = ? AND published = ? AND author = ? ;
    ''', (title, published, author ,))
    books_params = crsr.fetchall()
   
    return jsonify(books_params)
app.run()