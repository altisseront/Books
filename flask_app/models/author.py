from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def create( cls, data ):
        query = "INSERT INTO authors ( name , created_at , updated_at ) VALUES (%(name)s, NOW(), NOW());"
        connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        result = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in result:
            authors.append(cls(author))
        return authors

    @classmethod
    def get_author_favorites( cls, data ):
        query1 = "SELECT * FROM authors JOIN favorites ON authors.id = favorites.authors_id JOIN books ON books.id = favorites.books_id WHERE authors.id = %(author_id)s;"
        results1 = connectToMySQL('books_schema').query_db(query1, data)

        query2 = "SELECT * FROM authors WHERE authors.id = %(author_id)s;"
        results2 = connectToMySQL('books_schema').query_db(query2, data)
        author = cls(results2[0])
        for row in results1:
            book_data = {
            "id" : row['books.id'], 
            "title" : row['title'],
            "num_of_pages" : row['num_of_pages'],
            "created_at" : row['books.created_at'],
            "updated_at" : row['books.updated_at'],
            }
            author.books.append(book.Book(book_data))
        return author

    @classmethod
    def create_favorite(cls,data):
        query = "INSERT INTO favorites (authors_id, books_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)