# CLI Helper AddressBook

**CLI Helper** is a command-line application for managing personal contacts and notes. It allows users to add, edit, delete, and search contacts with support for names, phones, emails, addresses, and birthdays. The app also supports notes, persistent data storage, and user-friendly command parsing.

## 📦 Installation

You can install the package directly via pip:
pip install goit-dev-nest-addressbook-cli

🚀 Usage
Once installed, launch the assistant by running:
addressbook

You will see:
Welcome to the assistant bot!
Enter a command:

Now you can start using supported commands.

📚 Supported Commands
## Contact Management
- **add [name] [phone]** — Add a new contact or phone to an existing one
- **change [name] [old phone] [new phone]** — Change a phone number for a contact
- **phone [name]** — Show all phone numbers for a contact
- **add-email [name] [email]** — Add email to a contact
- **edit-email [name] [old email] [new email]** — Edit email for a contact
- **remove-email [name] [email]** — Remove email from a contact
- **add-address [name] [address...]** — Add address to a contact
- **edit-address [name] [new address...]** — Edit contact address
- **remove-address [name]** — Remove address
- **add-birthday [name] [DD.MM.YYYY]** — Add birthday
- **show-birthday [name]** — Show birthday
- **birthdays** — List contacts with birthdays in the next 7 days
- **all** — Show all contacts
- **search [query]** — Search contacts by name, phone, email, etc.

## Note Management
- **add-note [text]** — Add a new note
- **edit-note [index] [new text]** — Edit note by index
- **delete-note [index]** — Delete note by index
- **search-notes [query]** — Search notes by keyword
- **find-note-by-tag [tag]** — Find notes by tag
- **list-notes** — Show all notes

## Tag Management
- **add-tag [index] [tag]** — Add a tag to a note
- **remove-tag [index] [tag]** — Remove a tag from a note

## Other Commands
- **hello** — Greet the bot
- **exit, close** — Exit the assistant
🧠 Smart Suggestions
The app supports fuzzy matching. For example, if you mistype brthday, the app will suggest Did you mean: birthday?

💾 Persistence
Your address book is automatically saved to disk (addressbook.pkl) and restored on next launch.