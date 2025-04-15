import pickle
from addressbook.error_handler import input_error
from addressbook.address_book.address_book import AddressBook
from addressbook.note_book.note_book import NoteBook

ADDRESSBOOK_FILE = "addressbook.pkl"
NOTEBOOK_FILE = "notebook.pkl"

def save_addressbook(book: AddressBook, filename=ADDRESSBOOK_FILE):
    """Serialize the address book to a binary file."""
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
            print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_addressbook(filename=ADDRESSBOOK_FILE) -> AddressBook:
    """Deserialize the address book from a binary file or return a new book if not found."""
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            print(f"Data loaded from {filename}.")
            return book
    except FileNotFoundError:
        print("No existing address book found. Creating a new one.")
        return AddressBook()
    except Exception as e:
        print(f"Error loading data: {e}")
        return AddressBook()

def save_notebook(book: NoteBook, filename=NOTEBOOK_FILE):
    """Serialize the note book to a binary file."""
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
            print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_notebook(filename=NOTEBOOK_FILE) -> NoteBook:
    """Deserialize the note book from a binary file or return a new book if not found."""
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            print(f"Data loaded from {filename}.")
            return book
    except FileNotFoundError:
        print("No existing note book found. Creating a new one.")
        return NoteBook()
    except Exception as e:
        print(f"Error loading data: {e}")
        return NoteBook()

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args