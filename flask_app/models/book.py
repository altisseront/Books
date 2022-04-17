from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def create( cls, data ):
        query = "INSERT INTO books ( title , num_of_pages , created_at , updated_at ) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        result = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in result:
            books.append(cls(book))
        return books

    @classmethod
    def getBookWithFavorites(cls,data):
        query1 = "SELECT * FROM books JOIN favorites ON books.id = favorites.books_id JOIN authors ON authors.id = favorites.authors_id WHERE books.id = %(book_id)s;"

        results1 = connectToMySQL('books_schema').query_db(query1, data)

        query2 = "SELECT * FROM books WHERE books.id = %(book_id)s;"
        results2 = connectToMySQL('books_schema').query_db(query2, data)
        book = cls(results2[0])
        for row in results1:
            author_data = {
            "id" : row['authors.id'],
            "name" : row['name'],
            "created_at" : row['authors.created_at'],
            "updated_at" : row['authors.updated_at']
            }
            book.authors.append(author.Author(author_data))
        return book
    @classmethod
    def create_favorite(cls,data):
        query = "INSERT INTO favorites (authors_id, books_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)