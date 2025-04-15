import difflib
from colorama import Fore, Style, init

KNOWN_COMMANDS = [
    "add", "change", "phone", "all", 
    "add-birthday", "show-birthday", 
    "birthdays", "hello", "exit", "close",
    "add-email", "edit-email", "remove-email",
    "add-address", "edit-address", "remove-address",
    "add-note", "edit-note", "delete-note", "search-notes", "find-note-by-tag", "list-notes",
    "add-tag", "remove-tag"
]

def match_command(user_input: str, threshold=0.7):
    input_clean = user_input.strip().lower()
    closest = difflib.get_close_matches(input_clean, KNOWN_COMMANDS, n=1, cutoff=threshold)
    return closest[0] if closest else None

# Initialize colorama
init()

def print_commands():
    print("✅ print_commands() function was called")
    print(Fore.CYAN + "📚 Supported Commands")
    print(Fore.YELLOW + "\nContact Management")
    print(f"{Fore.GREEN}add{Style.BRIGHT} {Fore.YELLOW}[name] [phone]{Style.RESET_ALL} — Add a new contact or phone to an existing one")
    print(f"{Fore.GREEN}change{Style.BRIGHT} {Fore.YELLOW}[name] [old phone] [new phone]{Style.RESET_ALL} — Change a phone number for a contact")
    print(f"{Fore.GREEN}phone{Style.BRIGHT} {Fore.YELLOW}[name]{Style.RESET_ALL} — Show all phone numbers for a contact")
    print(f"{Fore.GREEN}add-email{Style.BRIGHT} {Fore.YELLOW}[name] [email]{Style.RESET_ALL} — Add email to a contact")
    print(f"{Fore.GREEN}edit-email{Style.BRIGHT} {Fore.YELLOW}[name] [old email] [new email]{Style.RESET_ALL} — Edit email for a contact")
    print(f"{Fore.GREEN}remove-email{Style.BRIGHT} {Fore.YELLOW}[name] [email]{Style.RESET_ALL} — Remove email from a contact")
    print(f"{Fore.GREEN}add-address{Style.BRIGHT} {Fore.YELLOW}[name] [address...]{Style.RESET_ALL} — Add address to a contact")
    print(f"{Fore.GREEN}edit-address{Style.BRIGHT} {Fore.YELLOW}[name] [new address...]{Style.RESET_ALL} — Edit contact address")
    print(f"{Fore.GREEN}remove-address{Style.BRIGHT} {Fore.YELLOW}[name]{Style.RESET_ALL} — Remove address")
    print(f"{Fore.GREEN}add-birthday{Style.BRIGHT} {Fore.YELLOW}[name] [DD.MM.YYYY]{Style.RESET_ALL} — Add birthday")
    print(f"{Fore.GREEN}show-birthday{Style.BRIGHT} {Fore.YELLOW}[name]{Style.RESET_ALL} — Show birthday")
    print(f"{Fore.GREEN}birthdays{Style.BRIGHT} {Style.RESET_ALL} — List contacts with birthdays in the next 7 days")
    print(f"{Fore.GREEN}all{Style.BRIGHT} {Style.RESET_ALL} — Show all contacts")
    print(f"{Fore.GREEN}search{Style.BRIGHT} {Fore.YELLOW}[query]{Style.RESET_ALL} — Search contacts by name, phone, email, etc.")
    print(Fore.YELLOW + "\nNote Management")
    print(f"{Fore.GREEN}add-note{Style.BRIGHT} {Fore.YELLOW}[text]{Style.RESET_ALL} — Add a new note")
    print(f"{Fore.GREEN}edit-note{Style.BRIGHT} {Fore.YELLOW}[index] [new text]{Style.RESET_ALL} — Edit note by index")
    print(f"{Fore.GREEN}delete-note{Style.BRIGHT} {Fore.YELLOW}[index]{Style.RESET_ALL} — Delete note by index")
    print(f"{Fore.GREEN}search-notes{Style.BRIGHT} {Fore.YELLOW}[query]{Style.RESET_ALL} — Search notes by keyword")
    print(f"{Fore.GREEN}find-note-by-tag{Style.BRIGHT} {Fore.YELLOW}[tag]{Style.RESET_ALL} — Find notes by tag")
    print(f"{Fore.GREEN}list-notes{Style.BRIGHT} {Style.RESET_ALL} — Show all notes")
    print(Fore.YELLOW + "\nTag Management")
    print(f"{Fore.GREEN}add-tag{Style.BRIGHT} {Fore.YELLOW}[index] [tag]{Style.RESET_ALL} — Add a tag to a note")
    print(f"{Fore.GREEN}remove-tag{Style.BRIGHT} {Fore.YELLOW}[index] [tag]{Style.RESET_ALL} — Remove a tag from a note")
    print(Fore.YELLOW + "\nOther Commands")
    print(f"{Fore.GREEN}hello{Style.BRIGHT} {Style.RESET_ALL} — Greet the bot")
    print(f"{Fore.GREEN}exit{Style.BRIGHT}, {Fore.GREEN}close{Style.BRIGHT} {Style.RESET_ALL} — Exit the assistant")