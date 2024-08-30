import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QComboBox, QTextEdit, QDialog
from services import BookService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Search")
        self.setGeometry(300, 200, 800, 600)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Buscar por autor, título o ISBN")
        self.search_input.setGeometry(20, 20, 560, 30)

        self.search_button = QPushButton("Buscar", self)
        self.search_button.setGeometry(600, 20, 80, 30)
        self.search_button.clicked.connect(self.search_books)

        self.results_table = QTableWidget(self)
        self.results_table.setGeometry(20, 60, 760, 400)
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["ID", "Título", "Autor", "ISBN"])

        self.details_button = QPushButton("Ver detalles", self)
        self.details_button.setGeometry(20, 480, 120, 30)
        self.details_button.clicked.connect(self.show_details)

        self.rate_button = QPushButton("Calificar libro", self)
        self.rate_button.setGeometry(160, 480, 120, 30)
        self.rate_button.clicked.connect(self.rate_book)

        self.review_button = QPushButton("Escribir reseña", self)
        self.review_button.setGeometry(300, 480, 120, 30)
        self.review_button.clicked.connect(self.write_review)

        self.insert_books_button = QPushButton("Insertar libros de prueba", self)
        self.insert_books_button.setGeometry(450, 480, 160, 30)
        self.insert_books_button.clicked.connect(self.insert_books)

        self.clear_db_button = QPushButton("Limpiar base de datos", self)
        self.clear_db_button.setGeometry(630, 480, 160, 30)
        self.clear_db_button.clicked.connect(self.clear_db)

        self.load_books()

    def load_books(self):
        books = BookService.get_books()
        self.results_table.setRowCount(len(books))
        for row, data in enumerate(books):
            for col, item in enumerate(data):
                self.results_table.setItem(row, col, QTableWidgetItem(str(item)))

    def search_books(self):
        query = self.search_input.text()
        results = BookService.search_books(query)
        self.results_table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, item in enumerate(data):
                self.results_table.setItem(row, col, QTableWidgetItem(str(item)))

    def show_details(self):
        selected_row = self.results_table.currentRow()
        if selected_row < 0:
            return

        book_id = int(self.results_table.item(selected_row, 0).text())
        self.details_window = DetailsWindow(book_id)
        self.details_window.show()

    def rate_book(self):
        selected_row = self.results_table.currentRow()
        if selected_row < 0:
            return

        book_id = int(self.results_table.item(selected_row, 0).text())
        self.rating_window = RatingWindow(book_id)
        self.rating_window.show()

    def write_review(self):
        selected_row = self.results_table.currentRow()
        if selected_row < 0:
            return

        book_id = int(self.results_table.item(selected_row, 0).text())
        self.review_window = ReviewWindow(book_id)
        self.review_window.show()

    def insert_books(self):
        BookService.insert_sample_books()
        self.search_books()

    def clear_db(self):
        BookService.clear_database()
        self.search_books()

class DetailsWindow(QDialog):
    def __init__(self, book_id):
        super().__init__()

        self.setWindowTitle("Detalles del libro")
        self.setGeometry(400, 300, 400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        book = BookService.get_book_details(book_id)
        layout.addWidget(QLabel(f"Título: {book[0]}"))
        layout.addWidget(QLabel(f"Autor: {book[1]}"))
        layout.addWidget(QLabel(f"ISBN: {book[2]}"))
        layout.addWidget(QLabel(f"Promedio de calificación: {book[3] if book[3] else 'Sin calificaciones'}"))

        self.reviews_table = QTableWidget(self)
        self.reviews_table.setColumnCount(3)
        self.reviews_table.setHorizontalHeaderLabels(["Usuario", "Calificación", "Reseña"])
        layout.addWidget(self.reviews_table)

        self.load_reviews(book_id)

    def load_reviews(self, book_id):
        reviews = BookService.get_reviews(book_id)
        self.reviews_table.setRowCount(len(reviews))
        for row, review in enumerate(reviews):
            for col, item in enumerate(review):
                self.reviews_table.setItem(row, col, QTableWidgetItem(str(item)))

class RatingWindow(QDialog):
    def __init__(self, book_id):
        super().__init__()

        self.setWindowTitle("Calificar libro")
        self.setGeometry(400, 300, 300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.rating_input = QLineEdit(self)
        self.rating_input.setPlaceholderText("Ingrese la calificación (1-5)")
        layout.addWidget(self.rating_input)

        self.submit_button = QPushButton("Enviar calificación", self)
        self.submit_button.clicked.connect(lambda: self.submit_rating(book_id))
        layout.addWidget(self.submit_button)

    def submit_rating(self, book_id):
        rating = self.rating_input.text()
        if not rating.isdigit() or not 1 <= int(rating) <= 5:
            return

        BookService.add_rating(book_id, int(rating))
        self.close()

class ReviewWindow(QDialog):
    def __init__(self, book_id):
        super().__init__()

        self.setWindowTitle("Escribir reseña")
        self.setGeometry(400, 300, 300, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.user_name_input = QLineEdit(self)
        self.user_name_input.setPlaceholderText("Ingrese su nombre")
        layout.addWidget(self.user_name_input)

        self.rating_input = QLineEdit(self)
        self.rating_input.setPlaceholderText("Ingrese la calificación (1-5)")
        layout.addWidget(self.rating_input)

        self.review_text_input = QTextEdit(self)
        self.review_text_input.setPlaceholderText("Escriba su reseña aquí")
        layout.addWidget(self.review_text_input)

        self.submit_button = QPushButton("Enviar reseña", self)
        self.submit_button.clicked.connect(lambda: self.submit_review(book_id))
        layout.addWidget(self.submit_button)

    def submit_review(self, book_id):
        user_name = self.user_name_input.text()
        rating = self.rating_input.text()
        review_text = self.review_text_input.toPlainText()

        if not user_name or not rating.isdigit() or not 1 <= int(rating) <= 5 or not review_text:
            return

        BookService.add_review(book_id, user_name, int(rating), review_text)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())