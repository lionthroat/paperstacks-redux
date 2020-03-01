import io
import csv
import pymysql
import pymysql.cursors
from app import app
from db import mysql
from flask import Flask, Response, render_template
from flask import request, redirect

@app.route('/')
def index():
    # query 1: get genre data for left sidebar links
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre order by genre.genre_name;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()

    # query 2: get featured book data (NOTE: maybe there is a way to randomize this?)
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
	select_stmt = "select book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id group by book.isbn order by book.book_title ASC;"
    # Note: groups by isbn so books with multiple authors only display once, however, only one author is shown.
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

@app.route('/add_book')
def add_book():
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('add_book.html', genres=GenresSQL)

@app.route('/add_author', methods=['POST','GET'])
def add_author():
    if request.method == 'GET':
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        select_stmt = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
        cursor.execute(select_stmt)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('add_author.html', books=result)

    elif request.method == 'POST':
        # Operation 1: Query to get max PK value of author_id
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT MAX(Authors.author_id) FROM Authors"
        cursor.execute(query)
        result = cursor.fetchall()
        author_id = result[0]['MAX(Authors.author_id)']
        author_id += 1
        cursor.close()
        connection.close()

        # Operation 2: Fetch Author information from form
        author_name = request.form['author_name']
        author_description = request.form['author_description']
        isbn = request.form['author_book']

        # Operation 3: Insert new Authors entry
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Authors (author_id, author_name, author_description) VALUES (%s,%s,%s)'
        values = (author_id, author_name, author_description)
        print("Values to be inserted are: ", values)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        # Operation 4: Insert Books_Authors entry to link new Author to Book
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
        values = (isbn, author_id)
        print("Values to be inserted are: ", values)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()

        return ('Author added!'); # NOTE: :( not a pretty page that displays, needs to redisplay regular website

#################################
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

# NOTE!!! Bug with this routing logic: it will only display genres for which there are books. This means you can't delete genres that have no books, which is a problem. Because of that, I haven't been able to test deleting genres yet.
@app.route('/genre/<string:id>/')
def genre(id):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, book.isbn, book.book_title, genre.genre_name from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genre.html', genreinfo=result)

@app.route('/add_genre', methods=['POST','GET'])
def add_genre():
    if request.method == 'GET':
        return render_template('add_genre.html')

    elif request.method == 'POST':
        # query 1: get max PK value of genre_id
        # NOTE: idk if there is a way to actually do "auto increment" or if we have to do it this way??
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT MAX(Genres.genre_id) FROM Genres"
        cursor.execute(query)
        result = cursor.fetchall()
        genre_id = result[0]['MAX(Genres.genre_id)']
        genre_id += 1
        cursor.close()
        connection.close()

        # query 2: insert new value to Genres
        # NOTE: this function doesn't check to make sure a genre with same name isn't already in database!!
        genre_name = request.form['genre_name']
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = 'INSERT INTO Genres (genre_id, genre_name) VALUES (%s,%s)'
        values = (genre_id, genre_name)
        print("Values to be inserted are: ", values)
        cursor.execute(query, values)
        connection.commit() # NOTE: entry will not be inserted w/o this
        cursor.close()
        connection.close()
        return ('Genre added!'); # NOTE: :( not a pretty page that displays, needs to redisplay regular website

@app.route('/rem_genre/<string:id>/', methods=['POST'])
# NOTE: I'm absolutely unsure what happens when you try to delete a genre that still has books associated with it
def rem_genre(id):
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM Genres WHERE Genres.genre_id = " + id
    cursor.execute(query)
    connection.commit() # NOTE: entry will not be removed w/o this
    cursor.close()
    connection.close()
    return ('Genre removed!'); # NOTE: :( not a pretty page, needs to redisplay regular website

@app.route('/add_review')
def add_review():
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
    cursor.execute(select_stmt)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('add_review.html', books=result)

@app.route('/search')
def search():
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre;"
    cursor.execute(select_stmt)
    GenresSQL = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('search.html', genres=GenresSQL)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()
