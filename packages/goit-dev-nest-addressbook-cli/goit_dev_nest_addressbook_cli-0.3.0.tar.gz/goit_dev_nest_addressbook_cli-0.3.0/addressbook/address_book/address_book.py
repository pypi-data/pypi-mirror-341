from collections import UserDict
from datetime import datetime, timedelta, date
from addressbook.error_handler import PhoneValidationError, BirthdayValidationError, AddressValidationError, EmailNotFound, EmailValidationError
import re

class Field:
    """
    Base class for all fields in a contact record.

    Attributes:
        value (str): The value of the field.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """
    Class for storing a contact's name.
    Inherits from Field.
    """
    pass

class Phone(Field):
    """
    Class for storing and validating a phone number.

    A valid phone number must consist of exactly 10 digits.
    """
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise PhoneValidationError()
        super().__init__(value)

class Birthday(Field):
    """
    Class for storing and validating a birthday date.

    The format must be 'dd.mm.yyyy'.
    """
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise BirthdayValidationError()
        
class Email(Field):
    """
    Class for storing and validating an email address.

    Uses a regular expression to check for proper format.
    """
    def __init__(self, value):
        if Email.is_valid_email(value):
            super().__init__(value)
        else:
            raise EmailValidationError

    @staticmethod
    def is_valid_email(value):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(pattern, value) is not None
    
class Address(Field):
    """
    Class for storing an address with a length limit.

    The address must not exceed 120 characters.
    """
    def __init__(self, value):
        if len(value) > 120:
            raise AddressValidationError() 
        super().__init__(value)

class Record:
    """
    Class for storing full contact information.

    Attributes:
        name (Name): The contact's name.
        phones (list): List of Phone objects.
        birthday (Birthday or None): Optional birthday.
        emails (list): List of Email objects.
        address (Address or None): Optional address.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None

    def add_phone(self, phone):
        """Adds a phone number to the contact."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Removes a phone number from the contact."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Edits an existing phone number."""
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        """Finds and returns a phone object by value."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str):
        """Adds a birthday to the contact."""
        self.birthday = Birthday(birthday_str)

    def add_email(self, email_str):
        """Adds an email address to the contact."""
        self.emails.append(Email(email_str))

    def edit_email(self, old_email, new_email):
          """Edits an existing email address."""
          for e in self.emails:
                if e.value == old_email: 
                    e.value = Email(new_email).value
                    return
          raise EmailNotFound
    
    def remove_email(self, email):
        """Removes an email address from the contact."""
        for e in self.emails:
            if e.value == email:
                self.emails.remove(e)
                return
        raise EmailNotFound
    
    def add_address(self, address_str):
        """Adds an address to the contact."""
        self.address = Address(address_str)

    def edit_address(self, address_str):
        """Updates the contact's address."""
        self.address = Address(address_str)

    def remove_address(self):
        """Removes the contact's address."""
        self.address = None
        
    def __str__(self):
        """Returns a formatted string representation of the contact."""
        phones = '; '.join(p.value for p in self.phones)
        bday = f"| Birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        emails = f"| Email: " + "; ".join(e.value for e in self.emails) if self.emails else ""
        address = f"| Address: {getattr(self, 'address', '')}" if getattr(self, 'address', '') else ""
        return f"Contact name: {self.name.value} | phones: {phones} {emails} {address} {bday}"

class AddressBook(UserDict):
    """
    Class for storing and managing a collection of contact records.

    Inherits from UserDict.
    """
    def add_record(self, record):
        """Adds a new record to the address book."""
        self.data[record.name.value] = record

    def find(self, name):
        """Finds a record by contact name."""
        return self.data.get(name)

    def delete(self, name):
        """Deletes a record by contact name."""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        """
        Returns a list of upcoming birthdays within the specified number of days.

        If a birthday falls on a weekend, the congratulation date is shifted to the next Monday.
        """
        today = datetime.today().date()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                name = record.name.value
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)
                    
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                days_until_birthday = (birthday_this_year - today).days
                
                if 0 <= days_until_birthday <= days:
                    if birthday_this_year.weekday() >= 5:  
                        while birthday_this_year.weekday() >= 5:
                            birthday_this_year += timedelta(days=1)
                    
                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays
