# Paperstacks Notes
## Last updated 3/9/2020

### Known Bugs:
- 3/9/2020: If an Author doesn't have a bio, their page will not display.
- 3/9/2020: Adding Authors may sometimes add them to the database twice.

### Recently Built Features:
- 3/9/2020: New redirect after adding new Author. Goes to /authors, displays success message, and highlights new Author in list.
- 3/9/2020: Delete an Author. Returns to /authors and displays success message.
- 3/9/2020: Update an Author
- 3/9/2020: Delete a Rating
- 3/9/2020: Edit a Rating
- 3/9/2020: Delete a Review
- 3/9/2020: Edit a Review
- 3/9/2020: Edit a Genre
- 3/8/2020: Genre Delete Validation. Before deleting a Genre from the database, there is now a preliminary SQL query that performs a COUNT(genre_id) to tally Books associated with a Genre. If this is a nonzero sum, the delete operation is aborted. The user then sees an error message as a <div> at the top of the page.
- 3/8/2020: Genre Delete. This routing and SQL already existed, but there had been no way to use it. Now, if a user successfully deletes a Genre from the database, they will be redirected to the main Genres page, and will see a success message in a <div> at the top of the page, which confirms the name of the Genre they removed.
- 3/7/2020: Upload Book Cover and Author Image (UI only at this point)
- 3/7/2020: Advanced Search Functionality (WIP). User can now perform a search from the navigation bar (a simple keyword search), or perform a more advanced search from the Search page or home page. In the advanced search, the user has the option of using one or more of the following criteria: book title (can be a substring), author name (can be a substring), year published, ISBN-10, or genre. Additional search criteria related to ratings/reviews not yet implemented.

### Recently Fixed Bugs:
- 3/9/2020: If an Author's bio has quotes in it, the Update function would fail because of lack of escape characters in the resulting string and SQL query. This was fixed using Python's built in replace() function that takes three parameters in the form of: string.replace(problem_substring, fixed_substring), and iterates through the string, replacing any instances of the first string with the second. This means you can create a string: quotes = "\"" and replace it with a fixed string: escaped_quotes = "\\\"".
- 3/8/2020: Reviews/Ratings displaying were displaying more than once because the SQL was not joining the 1:1 relationship properly between Ratings and Reviews to their associated Book, and then did not know how to handle NULL Reviews. This has been updated.
- 3/8/2020: Links to Book pages from an Author page now working. The routing was set to the relative URL 'book/<isbn>' (which resulted in the site-breaking link format 'author/121/book/393354377'), and needed to be changed to an absolute URL '/book/<isbn>'
- 3/8/2020: Individual Genre pages (at /genre/<id>) now display correctly even when they have no books associated with them. There needed to be additional Jinja templating
- 3/7/2020: Edit Book modal now pops up correctly. It was not opening due to the button being out of scope of the Jinja templating for loop which contained the book's information.
- 3/7/2020: CSS fixed so that styling now passed correctly to pages with dynamically generated content. This was also an issue with a relative vs. absolute URL, and had affected the navbar and other page elements.

### Still Needs to be Built Out:
- Book: remove (soft deadline 3/9/2020)
- Book: update (soft deadline 3/9/2020)
- Book: link to author page(s)
- Book: if no ratings and no reviews, state this and give user option to leave first one.
- Book: need to be able to list multiple authors
- Book: book covers not fully implemented
- Book: display average star rating

- Author: remove (soft deadline 3/9/2020)
- Author: pictures not fully implemented

- Authors: need modal to add new Author directly from this pages

- Search: by average star rating of books
- Search: by books that have reviews
- After adding a Book, Genre, Author, etc. the server returns a success message, which is a plain HTML message that takes the user away from the main site. We need to show the user a success message without seeming to depart from the site / take them away from navigation. Multiple possible options for this, including a pop-up, or a success message appended into the DOM.
- On Add Book: need more work to be able to add New Author at the same time. Currently does not read/store information from the modal.
- On Add Book: need additional server logic to check to see if a Book is being added without Author information (e.g. if they intend to add it later)
- On Add Book: need additional validation to see if user is attempting to add a Book that already exists. This screws up the insert so that other Book data may not be inserted correctly alongside the Book entry.
- On See All Books and individual Book pages, only one Author displays, even when there are multiple Authors. On Books, this is because I grouped by ISBN. Just needs to be tweaked, and Jinja code added to the HTML to display multiple authors when present. Logic can be copied from the Author page, where multiple books by same Author are shown.
- On Add Genre: Need additional validation to make sure user is not adding an existing Genre.
- On Add Book: Need additional validation to make sure user is not adding an existing Book.
- On Add Author: Need additional validation to make sure user is not adding an existing Author.

### Other Issues:
- General styling/commenting consistency in main python application. (Heather to comment certain passages better)
- Does the connection to db actually need to be closed after each query is executed within a view, or can we combine multiple actions that occur within the same function? This would save on a lot of lines of code, but if it allows data to get corrupt or is a security concern, then it needs to be left as is. Need to research best practices.
