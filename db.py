import sqlite3

DATABASE = 'books.db'

def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    conn = create_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            author TEXT,
                            isbn TEXT,
                            average_rating FLOAT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            book_id INTEGER,
                            user_name TEXT,
                            rating INTEGER,
                            review_text TEXT,
                            FOREIGN KEY(book_id) REFERENCES books(id))''')

def insert_sample_books():
    conn = create_connection()
    with conn:
        conn.execute("INSERT INTO books (title, author, isbn, average_rating) VALUES (?, ?, ?, ?)",
                     ('Clean Code', 'Robert C. Martin', '9780132350884', None))
        conn.execute("INSERT INTO books (title, author, isbn, average_rating) VALUES (?, ?, ?, ?)",
                     ('The Pragmatic Programmer', 'Andrew Hunt', '9780201616224', None))
        conn.execute("INSERT INTO books (title, author, isbn, average_rating) VALUES (?, ?, ?, ?)",
                     ('Introduction to Algorithms', 'Thomas H. Cormen', '9780262033848', None))
        conn.execute("INSERT INTO books (title, author, isbn, average_rating) VALUES (?, ?, ?, ?)",
                     ('Design Patterns: Elements of Reusable Object-Oriented Software', 'Erich Gamma', '9780201633610', None))

def clear_database():
    conn = create_connection()
    with conn:
        conn.execute("DELETE FROM books")
        conn.execute("DELETE FROM reviews")
    
    # Ejecutar VACUUM fuera de la transacción
    conn.execute("VACUUM")

def get_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, isbn FROM books")
    return cursor.fetchall()

def search_books(query):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, isbn FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?", 
                   ('%'+query+'%', '%'+query+'%', '%'+query+'%'))
    return cursor.fetchall()

def get_book_details(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, isbn, average_rating FROM books WHERE id = ?", (book_id,))
    return cursor.fetchone()

def get_reviews(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, rating, review_text FROM reviews WHERE book_id = ?", (book_id,))
    return cursor.fetchall()

def insert_review(book_id, user_name, rating, review_text):
    conn = create_connection()
    with conn:
        conn.execute("INSERT INTO reviews (book_id, user_name, rating, review_text) VALUES (?, ?, ?, ?)",
                     (book_id, user_name, rating, review_text))
        update_average_rating(book_id)

def insert_rating(book_id, rating):
    conn = create_connection()
    with conn:
        conn.execute("INSERT INTO reviews (book_id, rating) VALUES (?, ?)", (book_id, rating))
        update_average_rating(book_id)

def update_average_rating(book_id):
    conn = create_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(rating) FROM reviews WHERE book_id = ?", (book_id,))
        average_rating = cursor.fetchone()[0]
        if average_rating is None:
            average_rating = 0
        conn.execute("UPDATE books SET average_rating = ? WHERE id = ?", (average_rating, book_id))