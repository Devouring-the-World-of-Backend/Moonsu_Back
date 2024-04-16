document.addEventListener('DOMContentLoaded', function() {
    fetchBooks();

    document.getElementById('add-book-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const title = document.getElementById('title').value;
        const author = document.getElementById('author').value;
        const description = document.getElementById('description').value;
        const publishedYear = document.getElementById('published_year').value;
        
        const bookData = {
            title: title,
            author: author,
            description: description,
            published_year: parseInt(publishedYear),
        };
        
        addBook(bookData);
    });
});

function fetchBooks() {
    fetch('/books/')
        .then(response => response.json())
        .then(books => {
            const booksList = document.getElementById('books-list');
            booksList.innerHTML = '';
            books.forEach(book => {
                const bookItem = document.createElement('div');
                bookItem.className = 'book-item';
                bookItem.innerHTML = `<h3>${book.title}</h3><p>저자: ${book.author}</p><p>출판 연도: ${book.published_year}</p><p>${book.description}</p>`;
                booksList.appendChild(bookItem);
            });
        });
}

function addBook(bookData) {
    fetch('/books/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
    })
    .then(response => response.json())
    .then(book => {
        fetchBooks(); // 도서 목록 새로고침
    });
}
