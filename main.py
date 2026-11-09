import json
from pathlib import Path


class Book:
    def __init__(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available

    def to_dict(self):
        return {"title": self.title, "author": self.author, "available": self.available}


class Library:
    def __init__(self, data_file):
        self.data_file = Path(data_file)
        self.books = self.load()

    def load(self):
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
            return [Book(**item) for item in data]
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, TypeError, KeyError) as error:
            print(f"Could not load catalogue: {error}")
            return []

    def save(self):
        self.data_file.write_text(
            json.dumps([book.to_dict() for book in self.books], indent=2), encoding="utf-8"
        )

    def add(self, title, author):
        self.books.append(Book(title.strip(), author.strip()))
        self.save()

    def set_availability(self, title, available):
        for book in self.books:
            if book.title.casefold() == title.casefold():
                book.available = available
                self.save()
                return True
        return False


def main():
    library = Library(Path(__file__).with_name("books.json"))
    while True:
        print("\n1. List  2. Add  3. Borrow  4. Return  5. Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            if not library.books:
                print("The catalogue is empty.")
            for book in library.books:
                print(f"- {book.title} by {book.author} — {'available' if book.available else 'borrowed'}")
        elif choice == "2":
            title, author = input("Title: ").strip(), input("Author: ").strip()
            if title and author:
                library.add(title, author)
                print("Book saved.")
            else:
                print("Both title and author are required.")
        elif choice in {"3", "4"}:
            title = input("Title: ").strip()
            success = library.set_availability(title, choice == "4")
            print("Updated." if success else "No book with that title was found.")
        elif choice == "5":
            break
        else:
            print("Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
