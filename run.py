import time
from app import app
from SQLsafe import fetch, db_query, stringsafe
from flask import Flask, Response, render_template
from flask import request, redirect

# Main page
@app.route('/')
def index():
    select = "select genre.genre_id, genre.genre_name from Genres genre order by genre.genre_name"
    GenresSQL = fetch(select) # query 1: get genres for left sidebar links

    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id WHERE book.book_title = 'Electric Arches';"
    featuredBookSQL = fetch(select) # query 2: get featured book data

    return render_template('home.html', genres_list=GenresSQL, featuredbooks=featuredBookSQL)

# See a list of all books
@app.route('/books')
def books():
	select = "select book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id group by book.isbn order by book.book_title ASC;"
	result = fetch(select)
	return render_template('books.html', books=result)

# See a book
@app.route('/book/<string:isbn>/')
def book(isbn):
    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    BookSQL = fetch(select) # Step 1: Fetch Book's information

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 2: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 3: Fetch Book's Ratings that have no Review

    # Step 4: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    authors = fetch(select)

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, genres=genres, authors=authors)

# Add a new book
@app.route('/add_book', methods=['POST','GET'])
def add_book():
    if request.method == 'GET':
        select = "select genre.genre_id, genre.genre_name from Genres genre;"
        GenresSQL = fetch(select) # Get Genres information

        select = "select auth.author_id, auth.author_name from Authors auth;"
        AuthorsSQL = fetch(select) # Get Current Authors information

        return render_template('add_book.html', genres=GenresSQL, authors=AuthorsSQL)

    elif request.method == 'POST':
        # Operation 1: Fetch Book information from form
        book_title = request.form['book_title']
        isbn = request.form['book_isbn']
        year_published = request.form['book_year']

        book_description = request.form['book_description']
        book_description = stringsafe(book_description)

        genres = request.form.getlist('book_genre') # use getlist to get data from select multiple
        author_ids = request.form.getlist('book_author') # use getlist for select multiple

        query = 'INSERT INTO Books (isbn, book_title, year_published, book_description) VALUES (%s,%s,%s,%s)'
        values = (isbn, book_title, year_published, book_description)
        db_query(query, values) # Step 2: Insert new Book

        for author_id in author_ids:
            query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
            values = (isbn, author_id)
            db_query(query, values) # Step 3: Insert one or more Books_Authors entries

        for genre_id in genres:
            query = 'INSERT INTO Genres_Books (isbn, genre_id) VALUES (%s,%s)'
            values = (isbn, genre_id)
            db_query(query, values) # Step 4: Insert one or more Genres_Books entries

        return ("Book added! <a href='/'>(back to paperstacks)</a>");

# Edit a book
@app.route('/edit_book/<string:isbn>/', methods=['POST'])
def edit_book(isbn):
    # Update Book Title
    if request.form['update_title'] != '':
        title = request.form['update_title']
        title = stringsafe(title)
        title_string = ("'" + title + "'")
        query = "UPDATE Books SET book_title = %s WHERE isbn = %s"
        values = (title_string, isbn)
        db_query(query, values)

    # Update Book Description
    if request.form['update_book_description'] != '':
        description = request.form['update_book_description']
        description = stringsafe(description)  # add escape characters to single and double quotes
        description_string = ("'" + description + "'")
        query = "UPDATE Books SET book_description = %s WHERE isbn = %s"
        values = (description_string, isbn)
        db_query(query, values)

    if request.form['update_year'] != '':
        year = request.form['update_year']
        if (int(year) >= 0) and (int(year) < 2025):
            query = "UPDATE Books SET year_published = %s WHERE isbn = %s"
            values = (year, isbn)
            db_query(query, values)

    # if request.form['update_author'] != '':
    #     authors = request.form['update_author']

    # if request.form['update_genre'] != '':
    #     genres = request.form['update_genre']
    
    return("updated book <a href='/'>(back to paperstacks)</a>")
    # url = ("/book/" + isbn + "/edit_success/")
    # return redirect(url)

# BOOK EDITED SUCCESSFULLY, REDISPLAY BOOK PAGE
@app.route('/book/<string:isbn>/edit_book_success/')
def book_edited_successfully(isbn):
    book_edit = 1

    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    BookSQL = fetch(select) # Step 1: Fetch Book's information

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 2: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 3: Fetch Book's Ratings that have no Review

    # Step 4: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    authors = fetch(select)

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, book_edit=book_edit, genres=genres, authors=authors)

# DELETE A BOOK - MAJOR WIP!!!!!!!
@app.route('/rem_book/<string:isbn>/', methods=['POST'])
def rem_book(isbn):

    # Before removing a Book, check to make sure no Authors would be left without at least one Book
    select = "SELECT COUNT(genre.genre_id) AS `count` FROM Genres genre JOIN Genres_Books gb ON gb.genre_id = genre.genre_id JOIN Books book ON gb.isbn = book.isbn WHERE genre.genre_id = " + id
    result = fetch(select)

    # if there ARE books still in the genre
    # if result[0]['count'] != 0:
    #     url = ("/book/" + isbn + "/" + "error/")
    #     return redirect(url)

    # Delete Book
    # else:
    #     # get the name of the Genre we're removing
    #     connection = mysql.connect()
    #     cursor = connection.cursor(pymysql.cursors.DictCursor)
    #     select_stmt = "select genre.genre_name from Genres genre where genre.genre_id = " + id
    #     cursor.execute(select_stmt)
    #     result = cursor.fetchall()
    #     genre_to_remove = result[0]['genre_name']
    #     cursor.close()
    #     connection.close()
    #
    #     # delete the Genre
    #     connection = mysql.connect()
    #     cursor = connection.cursor(pymysql.cursors.DictCursor)
    #     query = "DELETE FROM Genres WHERE Genres.genre_id = " + id
    #     cursor.execute(query)
    #     connection.commit()
    #     cursor.close()
    #     connection.close()
    #
    #     # tell the user which Genre they have successfully removed,
    #     # and take them back to the main Genres page
    #     url = ("/genres/rem_success/" + genre_to_remove + "/")
    #     return redirect(url)
    return('yay, stuff')

# See a list of all authors
@app.route('/authors')
def authors():
	select_stmt = "select Authors.author_name, Authors.author_id from Authors order by Authors.author_name ASC;"
	result = fetch(select_stmt)
	return render_template('authors.html', authors=result)

# See one author
@app.route('/author/<string:author_id>/')
def author(author_id):
	select_stmt = "select auth.author_id, auth.author_name, auth.author_description, book.isbn, book.book_title from Authors auth join Books_Authors ba on ba.author_id = auth.author_id join Books book on book.isbn = ba.isbn where auth.author_id = " + author_id
	result = fetch(select_stmt)
	return render_template('author.html', author=result)

# Add a new author
@app.route('/add_author', methods=['POST','GET'])
def add_author():
    if request.method == 'GET':
        select_stmt = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
        result = fetch(select_stmt)
        return render_template('add_author.html', books=result)

    elif request.method == 'POST':
        query = "SELECT MAX(Authors.author_id) FROM Authors"
        result = fetch(select) # Step 1: Query to get max PK value of author_id
        author_id = result[0]['MAX(Authors.author_id)']
        author_id += 1

        # Step 2: Fetch Author information from form
        author_name = request.form['author_name']
        author_description = request.form['author_description']
        isbn = request.form['author_book']

        query = 'INSERT INTO Authors (author_id, author_name, author_description) VALUES (%s,%s,%s)'
        values = (author_id, author_name, author_description)
        db_query(query, values) # Step 3: Insert new Authors entry

        query = 'INSERT INTO Books_Authors (isbn, author_id) VALUES (%s,%s)'
        values = (isbn, author_id)
        db_query(query, values) # Step 4: Insert Books_Authors entry to link new Author to Book

        url = ("/authors/" + str(author_id) + "/add_success/" + author_name + "/")
        return redirect(url)

# Author was added successfully
@app.route('/authors/<string:author_id>/add_success/<string:author_name>/')
def successfully_added_author(author_id, author_name):
    id = int(author_id)
    result = fetch(select)
    return render_template('authors.html', authors=result, new_author=id, new_author_name=author_name)

# Edit an Author
@app.route('/edit_author/<string:author_id>/', methods=['POST'])
def edit_author(author_id):

    # Step 1: Update name
    name = request.form['update_author_name']
    name = stringsafe(name)
    name_string = ("'" + name + "'")
    query = "UPDATE Authors SET author_name = %s WHERE author_id = %s"
    values = (name_string, author_id)
    db_query(query, values)

    # Step 2: Update author bio
    bio = request.form['update_author_bio']
    bio = stringsafe(bio) # add escape characters to single and double quotes
    bio_string = ("'" + bio + "'")
    query = "UPDATE Authors SET author_description = %s WHERE author_id = %s"
    values = (bio_string, author_id)
    db_query(query, values)

    url = ("/author/" + author_id + "/edit_success/")
    return redirect(url)

# Author was edited successfully, redisplay author page.
@app.route('/author/<string:author_id>/edit_success/')
def successfully_edited_author(author_id):
    edit_success = 1
    select = "select auth.author_id, auth.author_name, auth.author_description, book.isbn, book.book_title from Authors auth join Books_Authors ba on ba.author_id = auth.author_id join Books book on book.isbn = ba.isbn where auth.author_id = " + author_id
    result = fetch(select)
    return render_template('author.html', author=result, edit_success=edit_success)

# Remove an author
@app.route('/rem_author', methods=['POST'])
def rem_author():
    author_id = request.form['author_id'] # Step 1: Get Author info

    query = "DELETE FROM Books_Authors WHERE Books_Authors.author_id = %s"
    values = (author_id)
    db_query(query, values)

    query = "DELETE FROM Authors WHERE Authors.author_id = %s"
    db_query(query, values)

    url = ("/authors/rem_success")
    return redirect(url)

# Author was removed successfully
@app.route('/authors/rem_success')
def successfully_deleted_author():
    rem_success = 1
    select = "select Authors.author_name, Authors.author_id from Authors order by Authors.author_name ASC;"
    result = fetch(select)
    return render_template('authors.html', authors=result, rem_success=rem_success)

@app.route('/genres')
def genres():
    select = "select genre.genre_id, genre.genre_name from Genres genre;"
    GenresSQL = fetch(select) # query 1: get genre data for list

    select = "select book.isbn, book.book_title, gb.genre_id FROM Books book JOIN Genres_Books gb ON gb.isbn = book.isbn"
    BooksSQL = fetch(select) # query 2: list books in each genre

    return render_template('genres.html', genres=GenresSQL, books=BooksSQL)

@app.route('/genre/<string:id>/')
def genre(id):
    # This first query returns only the genre name.
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre where genre.genre_id = " + id
    cursor.execute(select_stmt)
    genre_name= cursor.fetchall()
    cursor.close()
    connection.close()

    # Second query finds any books in that genre
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    cursor.execute(select_stmt)
    books_result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genre.html', genreinfo=genre_name, books=books_result)

# If cannot remove genre
@app.route('/genre/<string:id>/<string:error>/')
def cannot_remove_genre(id, error):
    # This first query returns only the genre name.
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select genre.genre_id, genre.genre_name from Genres genre where genre.genre_id = " + id
    cursor.execute(select_stmt)
    genre_name= cursor.fetchall()
    cursor.close()
    connection.close()

    # Second query finds any books in that genre
    connection = mysql.connect()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    select_stmt = "select book.isbn, book.book_title from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    cursor.execute(select_stmt)
    books_result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('genre.html', genreinfo=genre_name, books=books_result, error=error)

# Add a new Genre
@app.route('/add_genre', methods=['POST','GET'])
def add_genre():
    if request.method == 'GET':
        return render_template('add_genre.html')

    elif request.method == 'POST':
        select = "SELECT MAX(Genres.genre_id) FROM Genres"
        result = fetch(select) # query 1: get max PK value of genre_id
        genre_id = result[0]['MAX(Genres.genre_id)']
        genre_id += 1

        genre_name = request.form['genre_name']
        query = 'INSERT INTO Genres (genre_id, genre_name) VALUES (%s,%s)'
        values = (genre_id, genre_name)
        db_query(query, values) # query 2: insert new value to Genres

        return ("Genre added! <a href='/'>(back to paperstacks)</a>");

# Remove a Genre
@app.route('/rem_genre/<string:id>/', methods=['POST'])
def rem_genre(id):

    select = "SELECT COUNT(genre.genre_id) AS `count` FROM Genres genre JOIN Genres_Books gb ON gb.genre_id = genre.genre_id JOIN Books book ON gb.isbn = book.isbn WHERE genre.genre_id = " + id
    result = fetch(select) # Step 1: Check to make sure no Books associated with this Genre

    # if there ARE books still in the genre
    if result[0]['count'] != 0:
        url = ("/genre/" + id + "/" + "error/")
        print(url)
        return redirect(url)

    # Delete Genre
    else:
        select = "select genre.genre_name from Genres genre where genre.genre_id = " + id
        result = fetch(select) # get the name of the Genre we're removing
        genre_to_remove = result[0]['genre_name']

        query = "DELETE FROM Genres WHERE Genres.genre_id = %s"
        values = (id)
        db_query(query, values) # delete the Genre

        url = ("/genres/rem_success/" + genre_to_remove + "/")
        return redirect(url)

# Genre was removed successfully
@app.route('/genres/rem_success/<string:genre_name>/')
def successfully_deleted_genre(genre_name):

    select = "select genre.genre_id, genre.genre_name from Genres genre;"
    GenresSQL = fetch(select) # query 1: get genre data for list

    select = "select book.isbn, book.book_title, gb.genre_id FROM Books book JOIN Genres_Books gb ON gb.isbn = book.isbn"
    BooksSQL = fetch(select) # query 2: books in each genre

    return render_template('genres.html', genres=GenresSQL, books=BooksSQL, rem_success=genre_name)

# Edit a Genre
@app.route('/edit_genre/<string:genre_id>/', methods=['POST'])
def edit_genre(genre_id):
    new_name = request.form['update_genre_name']
    name_string = ("'" + new_name + "'")

    query = "UPDATE Genres SET genre_name = %s WHERE genre_id = %s"
    values = (name_string, genre_id)
    db_query(query, values)

    url = ("/genre/" + genre_id + "/edit_success/" + new_name + "/")
    print(url)
    return redirect(url)

# Successfully updated Genre name
@app.route('/genre/<string:id>/edit_success/<string:new_name>/')
def edit_genre_success(id, new_name):

    select = "select genre.genre_id, genre.genre_name from Genres genre where genre.genre_id = " + id
    genre_name = fetch(select) # returns only the genre name.

    select = "select book.isbn, book.book_title from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where genre.genre_id = " + id
    books_result = fetch(select) # Second query finds any books in that genre

    return render_template('genre.html', genreinfo=genre_name, books=books_result, new_name=new_name)

# Remove a Rating
@app.route('/rem_rating/<string:isbn>/<string:rating_id>/', methods=['POST'])
def rem_rating(isbn, rating_id):

    query = "DELETE FROM Ratings WHERE Ratings.rating_id = %s"
    values = (rating_id)
    db_query(query, values)

    url = ("/book/" + isbn + "/rem_rating_success/")
    return redirect(url)

# Rating removed, redisplay book page
@app.route('/book/<string:isbn>/rem_rating_success/')
def rating_removed_successfully(isbn):
    rating_rem = "The rating removal succeeded"

    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    BookSQL = fetch(select) # Step 1: Fetch Book's information

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 2: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 3: Fetch Book's Ratings that have no Review

    # Step 4: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    authors = fetch(select)

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, rating_rem=rating_rem, genres=genres, authors=authors)

# Remove a rating
@app.route('/rem_review/<string:isbn>/<string:review_id>/', methods=['POST'])
def rem_review(isbn, review_id):

    query = "DELETE FROM Reviews WHERE Reviews.review_id = %s"
    values = (review_id)
    db_query(query, values)

    url = ("/book/" + isbn + "/rem_review_success/")
    return redirect(url)

# Review removed, redisplay book page
@app.route('/book/<string:isbn>/rem_review_success/')
def review_removed_successfully(isbn):
    review_rem = "The review removal succeeded"

    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    BookSQL = fetch(select) # Step 1: Fetch Book's information

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 2: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 3: Fetch Book's Ratings that have no Review

    # Step 4: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    authors = fetch(select)

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, review_rem=review_rem, authors=authors, genres=genres)

# Edit review
@app.route('/edit_review/<string:isbn>/<string:review_id>/', methods=['POST'])
def edit_review(isbn, review_id):
    content = request.form['update_review_content']
    content_string = ("'" + content + "'")

    query = "UPDATE Reviews SET review_content = %d WHERE review_id = %s"
    values = (content_string, review_id)
    db_query(query, values)

    url = ("/book/" + isbn + "/rem_review_success/")
    return redirect(url)

# Review edited successfully
@app.route('/book/<string:isbn>/edit_rev_success/')
def review_edit_successfully(isbn):
    review_edit = "The review edit succeeded"

    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    BookSQL = fetch(select) # Step 1: Fetch Book's information

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 2: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 3: Fetch Book's Ratings that have no Review

    # Step 4: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    authors = fetch(select)

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, review_edit=review_edit, genres=genres, authors=authors)

# Add a new rating/review
@app.route('/add_review', methods=['POST','GET'])
def add_review():
    if request.method == 'GET':
        select = "select book.isbn, book.book_title from Books book order by book.book_title ASC;"
        result = fetch(select)
        return render_template('add_review.html', books=result)

    elif request.method == 'POST':
        # Step 1: Need new rating_id PK
        select = "SELECT MAX(Ratings.rating_id) FROM Ratings"
        result = fetch(select)
        rating_id = result[0]['MAX(Ratings.rating_id)']
        rating_id += 1

        # Step 2: Fetch form info for Rating
        isbn = request.form['author_book']
        star_rating = request.form['user_rating']
        rating_date = time.strftime('%Y-%m-%d')

        # Step 3: Insert Rating, Note: review_id initially disregarded as FK to avoid insert errors
        query = 'INSERT INTO Ratings (rating_id, isbn, star_rating, rating_date) VALUES (%s,%s,%s,%s)'
        values = (rating_id, isbn, star_rating, rating_date)
        db_query(query, values)

        # Step 4: If Review not empty...
        if request.form['user_review'] != '':
            # 4a. First, need a new review_id PK for our new Review entry
            select = "SELECT MAX(Reviews.review_id) FROM Reviews"
            result = fetch(select)
            review_id = result[0]['MAX(Reviews.review_id)']
            review_id += 1

            # 4b. Second, fetch Review info from form and system
            review_content = request.form['user_review']
            review_date = time.strftime('%Y-%m-%d')

            query = 'INSERT INTO Reviews (review_id, rating_id, isbn, review_content, review_date) VALUES (%s,%s,%s,%s,%s)'
            values = (review_id, rating_id, isbn, review_content, review_date)
            db_query(query, values) # 4c. Connect to database and add Review

            # 4d. Last, update the Rating we inserted above with FK review_id
            query = 'UPDATE Ratings set review_id = %s WHERE rating_id = %s'
            values = (review_id, rating_id)
            db_query(query, values)

        url = ("/book/" + isbn + "/add_rev_success/")
        return redirect(url)

# Review was added successfully
@app.route('/book/<string:isbn>/add_rev_success/')
def review_add_success(isbn):
    review_add = "The review add succeeded"

    select = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    BookSQL = fetch(select) # Step 1: Fetch Book's information

    select = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select) # Step 2: Fetch Book's Reviews with Ratings

    select = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select) # Step 3: Fetch Book's Ratings that have no Review

    # Step 4: For Edit Book Modal
    select = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    genres = fetch(select)
    select = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    authors = fetch(select)

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, review_add=review_add, genres=genres, authors=authors)

# Edit a star rating
@app.route('/edit_rating/<string:isbn>/<string:rating_id>/', methods=['POST'])
def edit_rating(isbn, rating_id):
    star_rating = request.form['update_rating']
    query = "UPDATE Ratings SET star_rating = %s WHERE rating_id = %s"
    values = (star_rating, rating_id)
    db_query(query, values)

    url = ("/book/" + isbn + "/edit_rating_success/")
    return redirect(url)

# Rating was edited successfully
@app.route('/book/<string:isbn>/edit_rating_success/')
def rating_edit_successfully(isbn):
    rating_edit = "The rating edit succeeded"

    select_stmt = "select book.isbn, book.book_title, book.year_published, book.book_description, auth.author_name, auth.author_id, genre.genre_name from Books book join Books_Authors ba on ba.isbn = book.isbn join Authors auth on auth.author_id = ba.author_id join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = " + isbn
    BookSQL = fetch(select_stmt) # Step 1: Fetch Book's information

    select_stmt = "select book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = " + isbn + " AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id"
    ReviewSQL = fetch(select_stmt) # Step 2: Fetch Book's Reviews with Ratings

    select_stmt = "SELECT * FROM Ratings WHERE isbn = " + isbn + " AND review_id IS NULL"
    RatingSQL = fetch(select_stmt) # Step 3: Fetch Book's Ratings that have no Review

    # Step 4: For Edit Book Modal
    select_stmt = "SELECT Genres.genre_id, Genres.genre_name FROM Genres"
    genres = fetch(select_stmt)
    select_stmt = "SELECT Authors.author_id, Authors.author_name FROM Authors"
    authors = fetch(select_stmt)

    return render_template('book.html', bookresult=BookSQL, reviews=ReviewSQL, ratings=RatingSQL, rating_edit=rating_edit, genres=genres, authors=authors)

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method == 'GET':
        select = "select genre.genre_id, genre.genre_name from Genres genre;"
        GenresSQL = fetch(select)
        return render_template('search.html', genres_list=GenresSQL)

    elif request.method == 'POST':

        # NAVBAR SEARCH
        if request.form['search_submit'] == 'navbar_search':
            search_query = request.form['tiny']
            search_string = ("'%" + search_query + "%'") # allows substring searches

            select = "select genre.genre_id, genre.genre_name from Genres genre;"
            GenresSQL = fetch(select) # retrieve genre data from database

            select = "SELECT book.isbn, book.book_title FROM Books book WHERE book.book_title LIKE" + search_string # put together final query
            books = fetch(select) # search 1: look for search term in Books

            select = "SELECT auth.author_id, auth.author_name FROM Authors auth WHERE auth.author_name LIKE " + search_string # put together final query
            authors = fetch(select) # search 2: look for search term in Authors

            select = "SELECT genre.genre_id, genre.genre_name FROM Genres genre WHERE genre.genre_name LIKE " + search_string # put together final query
            genres = fetch(select) # search 3: look for search term in Genres

            return render_template('search.html', search_query=search_query, genres_list=GenresSQL, books=books, authors=authors, genres=genres)

        # ADVANCED SEARCH
        elif request.form['search_submit'] == 'advanced_search':
            # fetch form data from advanced search on /search
            title = request.form['search_title']
            author = request.form['search_author']
            year = request.form['search_year']
            isbn = request.form['search_isbn']
            genre = request.form['search_genre']

            # advanced search operation 1: look for search term(s) in Books
            search_string = ("'%" + title + "%'") # allows substring search from book titles
            select_stmt = "SELECT book.isbn, book.book_title, auth.author_id, auth.author_name FROM Books book JOIN Books_Authors ba ON ba.isbn = book.isbn JOIN Authors auth ON auth.author_id = ba.author_id JOIN Genres_Books gb on gb.isbn = book.isbn JOIN Genres genre ON genre.genre_id = gb.genre_id WHERE " # put together final query

            query_num = 0
            if title != '':
                title_select = "book.book_title LIKE " + ("'%" + title + "%'")
                search_query = "Title: " + title

                select_stmt = select_stmt + title_select
                query_num += 1

            if year != '':
                if query_num != 0:
                    year_select = " AND book.year_published = " + year
                    search_query = search_query + ", Year Published: " + year
                else:
                    year_select = "book.year_published = " + year
                    search_query = "Year Published: " + year

                select_stmt = select_stmt + year_select
                query_num += 1

            if isbn != '':
                if query_num != 0:
                    isbn_select = " AND book.isbn = " + isbn
                    search_query = search_query + ", ISBN-10: " + isbn
                else:
                    isbn_select = "book.isbn = " + isbn
                    search_query = "ISBN-10: " + isbn

                select_stmt = select_stmt + isbn_select
                query_num += 1

            if author != '':
                if query_num != 0:
                    author_select = " AND auth.author_name LIKE " + ("'%" + author + "%'")
                    search_query = search_query + ", Author: " + author
                else:
                    author_select = "auth.author_name LIKE " + ("'%" + author + "%'")
                    search_query = "Author: " + author

                select_stmt = select_stmt + author_select
                query_num += 1

            if genre != '':
                if query_num != 0:
                    genre_select = " AND genre.genre_id = " + genre
                    search_query = search_query + ", Genre: " + genre
                else:
                    genre_select = "genre.genre_id = " + genre
                    search_query = "Genre: " + genre

                select_stmt = select_stmt + genre_select
                query_num += 1

            select_stmt = select_stmt + " GROUP BY book.isbn ORDER BY book.book_title ASC"
            books = fetch(select_stmt)

            # advanced search operation 2: look for search term(s) in Authors
            if author != '':
                search_string = ("'%" + author + "%'") # allows substring search from author names
                select = "SELECT auth.author_id, auth.author_name FROM Authors auth WHERE auth.author_name LIKE " + search_string # put together final query
                authorResult = fetch(select)
            else:
                authorResult = ''

            select = "select genre.genre_id, genre.genre_name from Genres genre;"
            GenresSQL = fetch(select) # Page display: retrieve genre data

            return render_template('search.html', search_query=search_query, genres_list=GenresSQL, books=books, authors=authorResult)

        else: # (user pressed search but didn't enter query)
            select = "select genre.genre_id, genre.genre_name from Genres genre;"
            GenresSQL = fetch(select)
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
