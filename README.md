# Redux notes:
## Last updated 3/1/2020

- Links to Book pages from an Author page aren't working. The routing is set to 'book/<isbn>' but when you're on an Author's page, you're already at 'author/<author_id>', so it just appends that to the relative URL and ends up looking like 'author/121/book/393354377', which breaks.
- On See All Books and individual Book pages, only one Author displays, even when there are multiple Authors. On Books, this is because I grouped by ISBN. Just needs to be tweaked, and logic added to the HTML to display multiple authors when present.
- Non-Bootstrap (custom) CSS not being passed to dynamically generated pages, affecting appearance of Navbar and other styled details.
