import io
import csv
import pymysql
from app import app
from db import mysql
from flask import Flask, Response, render_template

@app.route('/')
def index():
    # Want to implement counting books per genre... might need separate SQL for this?
    BooksPerGenre = []
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
    # query 1
    select_stmt = "select * from Genres;"
	cursor.execute(select_stmt)
	GenresSQL = cursor.fetchall()
    # query 2
	select_stmt = "select * from Books;"
	cursor.execute(select_stmt)
	BooksSQL = cursor.fetchall()
    # query 3
	select_stmt = "select * from Authors;"
	cursor.execute(select_stmt)
	AuthorsSQL = cursor.fetchall()

	cursor.close()
	connection.close()
    return render_template('home.html', genres=GenresSQL, books=BooksSQL, authors=AuthorsSQL, count=BooksPerGenre)

@app.route('/books')
def books():
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id order by book.book_title ASC;"
     # Note 1: might need to group by author once we implement multiple authors
     # Note 2: must select isbn here even though it's not displayed, as it's used to create
     #         the unique URL for each book page.
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('books.html', books=result)

@app.route('/book/<string:isbn>/')
def book(isbn):
	connection = mysql.connect()
	cursor = connection.cursor()
	select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('book.html', book=result)

if __name__ == "__main__":
    app.run()
