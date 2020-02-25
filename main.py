import io
import csv
import pymysql
from app import app
from db import mysql
from flask import Flask, Response, render_template

@app.route('/')
def index():
    # Want to implement this... how?
    BooksPerGenre = []
    return render_template('home.html', genres=Genres, books=Books, count=BooksPerGenre)

@app.route('/books')
def books():
	connection = mysql.connect()
	cursor = connection.cursor()
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
	# select_stmt = "SELECT Books.isbn, Books.book_title, Books.year_published, Books.book_description, Authors.author_name, Genres.genre_name FROM Books JOIN Authors ON Books.author_id = Authors.author_id JOIN Genres ON Books.genre_id = Genres.genre_id WHERE isbn = %(isbn)s;"
	# cursor.execute(select_stmt, { 'isbn': isbn })
	select_stmt = "SELECT Books.isbn, Books.book_title, Books.year_published, Books.book_description, Authors.author_name, Genres.genre_name FROM Books JOIN Authors ON Books.author_id = Authors.author_id JOIN Genres ON Books.genre_id = Genres.genre_id WHERE isbn = " + isbn
	cursor.execute(select_stmt)
	result = cursor.fetchall()
	cursor.close()
	connection.close()
	return render_template('book.html', book=result)

# @app.route('/download/report/csv')
# def download_report():
# 	conn = None
# 	cursor = None
# 	try:
# 		conn = mysql.connect()
# 		cursor = conn.cursor(pymysql.cursors.DictCursor)
#
# 		cursor.execute("SELECT emp_id, emp_first_name, emp_last_name, emp_designation FROM employee")
# 		result = cursor.fetchall()
#
# 		output = io.StringIO()
# 		writer = csv.writer(output)
#
# 		line = ['Emp Id, Emp First Name, Emp Last Name, Emp Designation']
# 		writer.writerow(line)
#
# 		for row in result:
# 			line = [str(row['emp_id']) + ',' + row['emp_first_name'] + ',' + row['emp_last_name'] + ',' + row['emp_designation']]
# 			writer.writerow(line)
#
# 		output.seek(0)
#
# 		return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=employee_report.csv"})
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close()
# 		conn.close()

if __name__ == "__main__":
    app.run()
