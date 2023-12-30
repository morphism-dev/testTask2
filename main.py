import sqlite3


class Library:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    description TEXT NOT NULL,
                    genre TEXT NOT NULL
                )
            ''')

    def select_genres(self):
        with self.conn:
            cursor = self.conn.execute('SELECT genre FROM books LIMIT 5')
            books = cursor.fetchall()
            if books != []:
                print('Добавленные жанры:')
                for i in books:
                    print(i[0])
                return True

    def add_book(self, title, author, description, genre):
        with self.conn:
            self.conn.execute('''
                INSERT INTO books (title, author, description, genre)
                VALUES (?, ?, ?, ?)
            ''', (title, author, description, genre))

    def view_books(self):
        with self.conn:
            cursor = self.conn.execute('SELECT id, title, author FROM books')
            return cursor.fetchall()

    def view_book_details(self, book_id):
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM books WHERE id = ?', (book_id,))
            return cursor.fetchone()

    def view_books_by_genre(self, genre):
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM books WHERE genre = ?', (genre,))
            return cursor.fetchall()

    def search_books(self, keyword):
        with self.conn:
            cursor = self.conn.execute('''
                SELECT id, title, author FROM books
                WHERE title LIKE ? OR author LIKE ?
            ''', ('%' + keyword + '%', '%' + keyword + '%'))
            return cursor.fetchall()

    def remove_book(self, book_id):
        with self.conn:
            self.conn.execute('DELETE FROM books WHERE id = ?', (book_id,))

    def close(self):
        self.conn.close()


def search_book_by_id(library, book_id):
    book_by_id = library.view_book_details(book_id)
    if book_by_id:
        print(f"Название: {book_by_id[1]}")
        print(f"Автор: {book_by_id[2]}")
        print(f"Описание: {book_by_id[3]}")
        print(f"Жанр: {book_by_id[4]}")
    else:
        print("Книга не найдена.")


def main():
    db_file = "library.db"
    library = Library(db_file)

    while True:
        print("\nМеню:")
        print("1. Добавить новую книгу")
        print("2. Просмотреть список книг")
        print("3. Поиск книги")
        print("4. Удалить книгу")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            description = input("Введите описание книги: ")
            library.select_genres()
            genre = input("Введите жанр книги: ")
            library.add_book(title, author, description, genre)
            print("Книга успешно добавлена в библиотеку.")

        elif choice == "2":
            print('1. Показать все книги')
            print('2. Показать книги определенного жанра')
            action = input("Выберите действие: ")
            if action == '1':
                books = library.view_books()
                if not books:
                    print("Библиотека пуста.")
                else:
                    print("Список книг:")
                    for book in books:
                        print(f"{book[0]}. {book[1]} - {book[2]}")
                    detailed_info = input(
                        'Введите ID книги подробную информацию про которую вы хотите получить, если нет то нажмите '
                        'Enter: ')
                    if detailed_info.isdigit():
                        search_book_by_id(library, detailed_info)
            elif action == '2':
                user_input_genre = input('Введите жанр: ')
                genre_books = library.view_books_by_genre(user_input_genre)
                if genre_books != []:
                    for i in genre_books:
                        print(f"{i[0]}. {i[1]} - {i[2]}")
                    detailed_info = input(
                        'Введите ID книги подробную информацию про которую вы хотите получить, если нет то нажмите '
                        'Enter: ')
                    if detailed_info.isdigit():
                        search_book_by_id(library, detailed_info)

        elif choice == "3":
            keyword = input("Введите ключевое слово или фразу для поиска: ")
            matching_books = library.search_books(keyword)
            if not matching_books:
                print(f"По запросу '{keyword}' книги не найдены.")
            else:
                print(f"Найденные книги по запросу '{keyword}':")
                for book in matching_books:
                    print(f"{book[0]}. {book[1]} - {book[2]}")

        elif choice == "4":
            books = library.view_books()
            if not books:
                print("Библиотека пуста.")
            else:
                book_id = int(input("Введите ID книги для удаления: "))
                library.remove_book(book_id)
                print("Книга удалена.")

        elif choice == "5":
            library.close()
            break


if __name__ == "__main__":
    main()
