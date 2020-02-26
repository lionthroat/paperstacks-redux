import io
import csv
import pymysql
import pymysql.cursors
from app import app
from db import mysql
from flask import Flask, Response, render_template

@app.route('/')
def index():
    # query 1: get genre data for left sidebar links
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # query 2: get featured book data (maybe there is a way to randomize this?)
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_book = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id WHERE book.book_title = 'Electric Arches';"
    cursor.execute(select_book)
    featuredBookSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('home.html', genres=GenresSQL, featuredbooks=featuredBookSQL)

@app.route('/books')
def books():
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id order by book.book_title ASC;"
     # Note 1: might need to group by author once we implement multiple authors
     # Note 2: must select isbn here even though it's not displayed, as it's used to create the unique URL for each book page.
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('books.html', books=result)

@app.route('/book/<string:isbn>/')
def book(isbn):
	connection = mysql.connect()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('book.html', bookresult=result)

@app.route('/genres')
def genres():
    # query 1: get genre data for list
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # query 2: get books data to list books in each genre category
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title, gb.genre_id FROM Books book JOIN Genres_Books gb ON gb.isbn = book.isbn"
    cursor.execute(select_stmt)
    BooksSQL = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genres.html', genres=GenresSQL, books=BooksSQL)

# @app.route('/genre/<string:id>/')
# def genre(id):
#     return render_template('genre.html', id=int(id), genres=Genres, books=Books)
if __name__ == "__main__":
    app.run()
