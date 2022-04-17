from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/')
def redir():
    return redirect('/authors')

@app.route('/authors')
def displayAuthors():
    return render_template('index.html', authors = Author.get_all())

@app.route('/create_author', methods = ['POST'])
def createAuthor():
    data = {
        "name" : request.form["name"]
    }
    Author.create(data)
    return redirect('/authors')

@app.route('/authors/<int:author_id>')
def showAuthorWithBooks(author_id):
    data = {
        "author_id" : author_id
    }
    return render_template('showauthor.html', author_with_favorites = Author.get_author_favorites(data), books = Book.get_all())

@app.route('/create_favorite_book/<int:author_id>', methods = ['POST'])
def createFavorite(author_id):
    data = {
        "book_id": request.form['title'],
        "author_id" : author_id
    }
    Author.create_favorite(data)
    return redirect(f'/authors/{author_id}')