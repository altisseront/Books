from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/books')
def displayBooks():
    return render_template('books.html', books = Book.get_all())

@app.route('/book_create', methods = ['POST'])
def createBook():
    data = {
        "title" : request.form["title"],
        "num_of_pages" : request.form["pages"]
    }
    Book.create(data)
    return redirect('/books')
@app.route('/books/<int:book_id>')
def getBookWithFavorites(book_id):
    data = {
        "book_id" : book_id
    }
    return render_template('showbook.html', book_with_favorites = Book.getBookWithFavorites(data), authors = Author.get_all())

@app.route('/add_favorite_author/<int:book_id>', methods = ['POST'])
def addFavorite(book_id):
    data = {
        "author_id": request.form['title'],
        "book_id" : book_id
    }
    Book.create_favorite(data)
    return redirect(f'/books/{book_id}')
