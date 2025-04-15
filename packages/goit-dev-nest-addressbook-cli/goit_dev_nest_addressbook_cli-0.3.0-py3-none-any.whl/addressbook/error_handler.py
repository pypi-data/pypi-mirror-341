from colorama import Fore, Style

class PhoneValidationError(ValueError):
    """Custom exception for phone validation errors."""
    pass

class BirthdayValidationError(ValueError):
    """Custom exception for birthday validation errors."""
    pass

class AddressValidationError(ValueError):
    """Custom exception for address validation errors."""
    pass

class EmailValidationError(ValueError):
    """Custom exception for email validation errors."""
    pass

class EmailNotFound(Exception):
    """Custom exception for not found email."""
    pass

class NoteNotFound(Exception):
    """Custom exception for not found note."""
    pass

class NoteExists(Exception):
    """Custom exception for overriding note."""
    pass

class TagNotFound(Exception):
    """Custom exception for not found tag."""
    pass

class TagExists(Exception):
    """Custom exception for overriding tag."""
    pass

class TitleValidationError(ValueError):
    """Custom exception for title validation errors."""
    pass

class ContentValidationError(ValueError):
    """Custom exception for content validation errors."""
    pass

class TagValidationError(ValueError):
    """Custom exception for tag validation errors."""
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return Fore.RED + "Contact not found." + Style.RESET_ALL
        except IndexError:
            return Fore.YELLOW + "Enter user name." + Style.RESET_ALL
        except PhoneValidationError:
            return Fore.YELLOW + "Phone must have exactly 10 digits." + Style.RESET_ALL
        except BirthdayValidationError:
            return Fore.YELLOW + "Birthday must be in DD.MM.YYYY format." + Style.RESET_ALL
        except AddressValidationError:
            return Fore.YELLOW + "Address is too long. It must be 120 characters or fewer." + Style.RESET_ALL
        except EmailValidationError:
            return Fore.YELLOW + "Please enter Name and email" + Style.RESET_ALL
        except TitleValidationError:
            return Fore.YELLOW + "Title of length under 100 characters is required" + Style.RESET_ALL
        except ContentValidationError:
            return Fore.YELLOW + "Content of length under 500 characters is required" + Style.RESET_ALL
        except TagValidationError:
            return Fore.YELLOW + "Tag of length under 50 characters is required" + Style.RESET_ALL
        except EmailNotFound:
            return Fore.RED + "Email not found" + Style.RESET_ALL
        except NoteNotFound:
            return Fore.RED + "Note not found" + Style.RESET_ALL
        except TagNotFound:
            return Fore.RED + "Tag not found" + Style.RESET_ALL
        except TagExists:
            return Fore.RED + "Tag already exists" + Style.RESET_ALL
        except NoteExists:
            return Fore.RED + "Note already exists" + Style.RESET_ALL
        except ValueError:
            return Fore.YELLOW + "Give me name and phone please." + Style.RESET_ALL
    return inner