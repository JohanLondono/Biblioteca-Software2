import db

class BookService:
    @staticmethod
    def get_books():
        return db.get_books()

    @staticmethod
    def search_books(query):
        return db.search_books(query)

    @staticmethod
    def get_book_details(book_id):
        return db.get_book_details(book_id)

    @staticmethod
    def get_reviews(book_id):
        return db.get_reviews(book_id)

    @staticmethod
    def add_review(book_id, user_name, rating, review_text):
        db.insert_review(book_id, user_name, rating, review_text)

    @staticmethod
    def add_rating(book_id, rating):
        db.insert_rating(book_id, rating)

    @staticmethod
    def insert_sample_books():
        db.insert_sample_books()

    @staticmethod
    def clear_database():
        db.clear_database()