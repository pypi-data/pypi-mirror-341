from addressbook.utils import parse_input, save_addressbook, load_addressbook, load_notebook, save_notebook
from addressbook.address_book.handlers import add_contact, edit_contact, get_contact, birthdays, add_birthday, show_birthday, add_email, edit_email, remove_email, show_all, add_address, edit_address, remove_address
from addressbook.note_book.handlers import add_note, edit_note, delete_note, search_note, find_note_by_tag, list_notes, add_tag, remove_tag
from addressbook.command_matcher import match_command, KNOWN_COMMANDS, print_commands
from colorama import init, Fore, Back, Style

def main():
    addressbook = load_addressbook()
    notebook = load_notebook()
    print_commands()
    print()
    print(Back.CYAN + Fore.BLACK + "Welcome to the assistant bot version 0.3.0!" + Style.RESET_ALL)
    while True:
        user_input = input(Fore.MAGENTA + "Enter a command: " + Style.RESET_ALL)
        command, *args = parse_input(user_input)

        if command not in KNOWN_COMMANDS:
            suggestion = match_command(command)
            if suggestion:
                confirm = input(Fore.YELLOW + f"Did you mean '{suggestion}'? (y/n): " + Style.RESET_ALL)
                if confirm.lower() == "y":
                    command = suggestion
                else:
                    print(Fore.RED + "Unknown command." + Style.RESET_ALL)
                    continue
            else:
                print(Fore.RED + "Unknown command." + Style.RESET_ALL)
                continue

        match command:
            case x if x in ["close", "exit"]:
                save_addressbook(addressbook)
                save_notebook(notebook)
                print(Back.CYAN + Fore.BLACK + "Good bye!" + Style.RESET_ALL)
                break
            case "hello":
                print(Fore.MAGENTA + "How can I help you?" + Style.RESET_ALL)
            case "add":
                print(add_contact(args,addressbook))
            case "change":
                print(edit_contact(args,addressbook))
            case "phone":
                print(get_contact(args,addressbook))
            case "all":
                print(show_all(args,addressbook))
            case "add-birthday":
                print(add_birthday(args,addressbook))
            case "show-birthday":
                print(show_birthday(args,addressbook))
            case "birthdays":
                print(birthdays(args,addressbook))
            case "add-email":
                print(add_email(args,addressbook))
            case "edit-email":
                print(edit_email(args,addressbook))
            case "remove-email":
                print(remove_email(args,addressbook))
            case "add-address":
                print(add_address(args,addressbook))
            case "edit-address":
                print(edit_address(args,addressbook))
            case "remove-address":
                print(remove_address(args,addressbook))
            case "add-note":
                print(add_note(args, notebook))
            case "edit-note":
                print(edit_note(args, notebook))
            case "delete-note":
                print(delete_note(args, notebook))
            case "search-notes":
                print(search_note(args, notebook))
            case "find-note-by-tag":
                print(find_note_by_tag(args, notebook))
            case "list-notes": 
                print(list_notes(args, notebook))
            case "add-tag": 
                print(add_tag(args, notebook))
            case "remove-tag": 
                print(remove_tag(args, notebook))
            case _:
                print(Fore.RED + "Invalid command." + Style.RESET_ALL)

if __name__ == "__main__":
    main()