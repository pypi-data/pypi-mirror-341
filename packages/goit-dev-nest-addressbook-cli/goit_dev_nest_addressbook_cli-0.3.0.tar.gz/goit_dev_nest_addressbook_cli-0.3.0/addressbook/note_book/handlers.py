from addressbook.note_book.note_book import NoteBook, Note
from addressbook.error_handler import input_error, EmailValidationError, EmailNotFound
from colorama import init, Fore, Back, Style

@input_error
def add_note(args, notebook):
    if not args:
        return Fore.YELLOW + "Please provide the note title and text." + Style.RESET_ALL
    title = args[0]
    text = " ".join(args[1:])
    if not text:
        return Fore.YELLOW + "Note text is required." + Style.RESET_ALL
    note = Note(title, text)
    notebook.add_note(note)
    return Fore.GREEN + "Note added." + Style.RESET_ALL


@input_error
def edit_note(args, notebook):
    if len(args) < 2:
        return Fore.YELLOW + "Usage: edit-note [title] [new text]" + Style.RESET_ALL
    title = args[0]
    new_text = " ".join(args[1:])
    notebook.change_note(title, new_text)
    return Fore.GREEN + f"Note '{title}' updated." + Style.RESET_ALL


@input_error
def delete_note(args, notebook):
    if not args:
        return Fore.YELLOW + "Usage: delete-note [title]" + Style.RESET_ALL
    title = args[0]
    result = notebook.delete_note(title)
    return  Fore.GREEN + "Note deleted" + Style.RESET_ALL


@input_error
def search_note(args, notebook):
    if not args:
        return Fore.YELLOW + "Please provide a title." + Style.RESET_ALL
    title = args[0]
    result = notebook.find_note_by_title(title)
    if not result:
        return Fore.YELLOW + "No notes found." + Style.RESET_ALL
    return result

@input_error
def find_note_by_tag(args, notebook):
    if not args:
        return Fore.YELLOW + "Please provide a tag to search." + Style.RESET_ALL
    tag = args[0]
    results = notebook.find_notes_by_tag(tag)
    if not results:
        return Fore.YELLOW + f"No notes with tag '{tag}' found." + Style.RESET_ALL
    return "\n".join(str(note) for note in results)

@input_error
def list_notes(args, notebook):
    if not notebook.notes:
        return Fore.YELLOW + "No notes available." + Style.RESET_ALL
    return "\n".join(f"{i}: {note}" for i, note in enumerate(notebook.notes))

@input_error
def add_tag(args, notebook):
    if len(args) < 2:
        return Fore.YELLOW + "Usage: add-tag [note_title] [tag]" + Style.RESET_ALL
    title = args[0]
    tag_value = args[1]
    return Fore.GREEN + notebook.add_tag_to_note(title, tag_value) + Style.RESET_ALL

@input_error
def remove_tag(args, notebook):
    if len(args) < 2:
        return Fore.YELLOW + "Usage: remove-tag [note_title] [tag]" + Style.RESET_ALL
    title = args[0]
    tag_value = args[1]
    return Fore.GREEN + notebook.remove_tag_from_note(title, tag_value) + Style.RESET_ALL