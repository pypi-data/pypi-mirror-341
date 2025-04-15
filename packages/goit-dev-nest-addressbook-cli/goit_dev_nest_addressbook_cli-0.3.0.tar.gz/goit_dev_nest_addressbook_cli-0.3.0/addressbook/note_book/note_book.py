from addressbook.error_handler import TagValidationError, ContentValidationError, TitleValidationError, TagNotFound, TagExists, NoteNotFound, NoteExists

class Title:
    def __init__(self, value):
        if not value:
            raise TitleValidationError
        if len(value) > 100:
            raise TitleValidationError
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Content: 
    def __init__(self, value):
        if value is None:
            value = ""
        if len (value) > 500:
            raise ContentValidationError
        self.value = value

    def __str__(self):
        return str(self.value)
        
class Tag:
    def __init__(self, value):
        if not value:
            raise TagValidationError
        if len(value) > 50:
            raise TagValidationError
        self.value = value

    def __str__(self):
        return self.value

class Note:
    def __init__(self, title, content=None, tags=None):
        if not title:
            raise TitleValidationError
        self.title = Title(title)
        self.content = Content(content)
        self.tags = [Tag(tag) for tag in tags] if tags else []
    
    def __str__(self):
        title_str = f"Title: {self.title.value}"
        content_str = f"Content: {self.content.value}"
        tags_str = f"Tags: {', '.join(str(tag) for tag in self.tags)}" if self.tags else ""
        return " | ".join(filter(None, [title_str, content_str, tags_str]))
    
class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        if self.find_note_by_title(note.title):
            raise ValueError("Note with this title already exists.")
        self.notes.append(note)
        return "Note added successfully :)"

    def find_note_by_title(self, title):
        title_str = title.value if isinstance(title, Title) else title
        if not title_str or title_str.strip() == "":
            return None
        for note in self.notes:
            if note.title.value == title_str:
                return note
        return None

    def find_notes_by_tag(self, tag_query):
        if not tag_query or tag_query.strip() == "":
            raise TagValidationError

        found_notes = []
        for note in self.notes:
            if any(tag.value.lower() == tag_query.lower() for tag in note.tags):
                found_notes.append(note)

        if not found_notes:
            return None

        return found_notes
    
    def show_note(self, title):
        note = self.find_note_by_title(title)
        if note:
            return f"Found note:\n{note}"
        else:
            return "Note not found"
    
    def change_note(self, title, new_content):
        note = self.find_note_by_title(title)
        if note: 
            note.content = Content(new_content) if new_content else note.content
            return "Note updated successfully"
        else:
            return "Note not found"
        
    def delete_note(self, title):
        note = self.find_note_by_title(title)
        if note:
            self.notes.remove(note)
            return "Note deleted successfully"
        else:
            return "Note not found"
        
    def show_all_notes(self):
        if not self.notes:
            return "You do not have any notes yet..."
        
        divider = "=" * 50
        return "\n".join(f"{divider}\n{note}\n{divider}" for note in self.notes)


    def add_tag_to_note(self, title, tag_value):
        note = self.find_note_by_title(title)
        if not note:
            raise NoteNotFound
        if any(tag.value == tag_value for tag in note.tags):
            raise TagExists
        note.tags.append(Tag(tag_value))
        return f"Tag '{tag_value}' added to note '{title}'"

    def remove_tag_from_note(self, title, tag_value):
        note = self.find_note_by_title(title)
        if not note:
            raise NoteNotFound
        for tag in note.tags:
            if tag.value == tag_value:
                note.tags.remove(tag)
                return f"Tag '{tag_value}' removed from note '{title}'"
        raise TagNotFound