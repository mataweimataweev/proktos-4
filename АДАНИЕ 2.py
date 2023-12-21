import sqlite3
import hashlib

class LibrarySystem:
    def __init__(self):
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                genre TEXT,
                availability INTEGER
            )
        ''')

        self.conn.commit()

    def register_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, hashed_password))
            self.conn.commit()
            print("Регистрация прошла успешно")
        except sqlite3.IntegrityError:
            print("Пользователь с таким именем уже существует")

    def login_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('SELECT * FROM Users WHERE username=? AND password=?', (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            print("Авторизация успешна")
        else:
            print("Неверное имя пользователя или пароль")

    def add_book(self, title, author, genre, availability=1):
        try:
            self.cursor.execute('INSERT INTO Books (title, author, genre, availability) VALUES (?, ?, ?, ?)',
                                (title, author, genre, availability))
            self.conn.commit()
            print("Книга успешно добавлена")
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении книги: {e}")

    def update_book(self, book_id, new_availability):
        try:
            self.cursor.execute('UPDATE Books SET availability=? WHERE book_id=?', (new_availability, book_id))
            self.conn.commit()
            print("Информация о книге успешно обновлена")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении информации о книге: {e}")

    def delete_book(self, book_id):
        try:
            self.cursor.execute('DELETE FROM Books WHERE book_id=?', (book_id,))
            self.conn.commit()
            print("Книга успешно удалена")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении книги: {e}")

    def filter_books(self, genre):
        try:
            self.cursor.execute('SELECT * FROM Books WHERE genre=?', (genre,))
            books = self.cursor.fetchall()
            if books:
                print("Найденные книги:")
                for book in books:
                    print(book)
            else:
                print("Книги по указанному жанру не найдены")
        except sqlite3.Error as e:
            print(f"Ошибка при фильтрации книг: {e}")

    def close_connection(self):
        self.conn.close()

# Пример использования
if __name__ == "__main__":
    library_system = LibrarySystem()

    while True:
        print("\n--- Меню ---")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Добавить книгу")
        print("4. Фильтровать книги по жанру")
        print("5. Обновить информацию о книге")
        print("6. Удалить книгу")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            library_system.register_user(username, password)

        elif choice == "2":
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            library_system.login_user(username, password)

        elif choice == "3":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            genre = input("Введите жанр книги: ")
            library_system.add_book(title, author, genre)

        elif choice == "4":
            genre = input("Введите жанр для фильтрации книг: ")
            library_system.filter_books(genre)

        elif choice == "5":
            book_id = input("Введите ID книги: ")
            new_availability = input("Введите новую доступность книги (0 или 1): ")
            library_system.update_book(int(book_id), int(new_availability))

        elif choice == "6":
            book_id = input("Введите ID книги для удаления: ")
            library_system.delete_book(int(book_id))

        elif choice == "0":
            library_system.close_connection()
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите существующий пункт меню.")
