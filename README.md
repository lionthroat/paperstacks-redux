# Paperstacks (Redux) Notes
## Last updated 3/8/2020

### Known Bugs:
- Reviews/Ratings displaying twice each on some Book pages. Issue with SQL to be fixed.

### Recently Built Features:
- 3/8/2020: Genre Delete Validation. Before deleting a Genre from the database, there is now a preliminary SQL query that performs a COUNT(genre_id) to tally Books associated with a Genre. If this is a nonzero sum, the delete operation is aborted. The user then sees an error message as a <div> at the top of the page.
- 3/8/2020: Genre Delete. This routing and SQL already existed, but there had been no way to use it. Now, if a user successfully deletes a Genre from the database, they will be redirected to the main Genres page, and will see a success message in a <div> at the top of the page, which confirms the name of the Genre they removed.
- 3/7/2020: Edit Book Modal.
- 3/7/2020: Upload Book Cover and Author Image.
- 3/7/2020: Advanced Search Functionality (WIP). User can now perform a search from the navigation bar (a simple keyword search), or perform a more advanced search from the Search page or home page. In the advanced search, the user has the option of using one or more of the following criteria: book title (can be a substring), author name (can be a substring), year published, ISBN-10, or genre. Additional search criteria related to ratings/reviews not yet implemented.

### Recently Fixed Bugs:
- 3/8/2020: Reviews/Ratings displaying were displaying more than once because the SQL was not joining the 1:1 relationship properly between Ratings and Reviews to their associated Book, and then did not know how to handle NULL Reviews. This has been updated.
- 3/8/2020: Links to Book pages from an Author page now working. The routing was set to the relative URL 'book/<isbn>' (which resulted in the site-breaking link format 'author/121/book/393354377'), and needed to be changed to an absolute URL '/book/<isbn>'
- 3/8/2020: Individual Genre pages (at /genre/<id>) now display correctly even when they have no books associated with them. There needed to be additional Jinja templating
- 3/7/2020: Edit Book modal now pops up correctly. It was not opening due to the button being out of scope of the Jinja templating for loop which contained the book's information.
- 3/7/2020: CSS fixed so that styling now passed correctly to pages with dynamically generated content. This was also an issue with a relative vs. absolute URL, and had affected the navbar and other page elements.

### Still Needs to be Built Out:
- Update/Remove Ratings (soft deadline 3/9/2020)
- Update/Remove Reviews (soft deadline 3/9/2020)
- Update/Remove Books (soft deadline 3/9/2020)
- Update/Remove Authors (soft deadline 3/9/2020)
- Book covers not fully implemented
- Author pictures not fully implemented
- Advanced search not completed
- Display and search by average star rating of books
- Search by books that have reviews
- After adding a Book, Genre, Author, etc. the server returns a success message, which is a plain HTML message that takes the user away from the main site. We need to show the user a success message without seeming to depart from the site / take them away from navigation. Multiple possible options for this, including a pop-up, or a success message appended into the DOM.
- On Add Book: need more work to be able to add New Author at the same time. Currently does not read/store information from the modal.
- On Add Book: need additional server logic to check to see if a Book is being added without Author information (e.g. if they intend to add it later)
- On Add Book: need additional validation to see if user is attempting to add a Book that already exists. This screws up the insert so that other Book data may not be inserted correctly alongside the Book entry.
- On See All Books and individual Book pages, only one Author displays, even when there are multiple Authors. On Books, this is because I grouped by ISBN. Just needs to be tweaked, and Jinja code added to the HTML to display multiple authors when present. Logic can be copied from the Author page, where multiple books by same Author are shown.
- On Add Genre: Need additional validation to make sure user is not adding an existing Genre.
- On Add Book: Need additional validation to make sure user is not adding an existing Book.
- On Add Author: Need additional validation to make sure user is not adding an existing Author.

### Known Bugs:
- None currently

### Other Issues:
- General styling/commenting consistency in main python application. (Heather to comment certain passages better)
- Does the connection to db actually need to be closed after each query is executed within a view, or can we combine multiple actions that occur within the same function? This would save on a lot of lines of code, but if it allows data to get corrupt or is a security concern, then it needs to be left as is. Need to research best practices.
