import json
import os
from typing import List, Dict, Optional


class BookManager:
    def __init__(self, data_file: str = "books.json"):
        """
        Инициализирует список книг, загружая данные из указанного файла.
        """
        self.data_file = data_file
        self.books = self.load_books()

    def load_books(self) -> List[Dict]:
        """
        Загружает данные из JSON-файла.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                return json.load(file)
        return []

    def save_books(self):
        """
        Сохраняет текущий список книг в JSON-файл.
        """
        with open(self.data_file, "w") as file:
            json.dump(self.books, file, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.
        title: Название книги.
        author: Автор книги.
        year: Год издания книги.
        """
        new_book = {
            "id": self.books[-1]['id'] + 1 if self.books else 1,
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии"
        }
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {new_book['id']}.")

    def delete_book(self, book_id: int):
        """
        Удаляет книгу по ID.
        """
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, key: str, value: str):
        """
        Ищет книги по указанному полю.
        key: Поле для поиска (title, author или year).
        value: Значение для поиска.
        """
        results = [book for book in self.books if str(book.get(key, "")).lower() == value.lower()]
        if results:
            self.display_books(results)
        else:
            print(f"Книги по запросу '{value}' не найдены.")

    def change_status(self, book_id: int, status: str):
        """
        Изменяет статус книги по ID.
        book_id: ID книги.
        status: Новый статус ("в наличии" или "выдана").
        """
        book = self.find_book_by_id(book_id)
        if book:
            if status in ["в наличии", "выдана"]:
                book["status"] = status
                self.save_books()
                print(f"Статус книги с ID {book_id} обновлен на '{status}'.")
            else:
                print("Неверный статус. Укажите 'в наличии' или 'выдана'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def display_books(self, books: Optional[List[Dict]] = None):
        """
        Отображает список книг.
        books: Список книг для отображения (если None, отображаются все книги).
        """
        books = books or self.books
        if books:
            for book in books:
                print(f"{book['id']}: {book['title']} - {book['author']} ({book['year']}) [{book['status']}]")
        else:
            print("Библиотека пуста.")

    def find_book_by_id(self, book_id: int) -> Optional[Dict]:
        """
        Находит книгу по ID.
        Возвращает Книгу, если найдена, иначе None.
        """
        return next((book for book in self.books if book["id"] == book_id), None)


def main():
    manager = BookManager()
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Выберите действие (1-6): ")

        try:
            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                manager.add_book(title, author, year)
            elif choice == "2":
                book_id = int(input("Введите ID книги: "))
                manager.delete_book(book_id)
            elif choice == "3":
                key = input("Искать по (title, author, year): ").lower()
                value = input("Введите значение для поиска: ")
                manager.search_books(key, value)
            elif choice == "4":
                manager.display_books()
            elif choice == "5":
                book_id = int(input("Введите ID книги: "))
                status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                manager.change_status(book_id, status)
            elif choice == "6":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
