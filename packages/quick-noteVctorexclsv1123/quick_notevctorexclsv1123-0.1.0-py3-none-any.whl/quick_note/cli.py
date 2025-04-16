import sys
import os

NOTES_FILE = "notes.txt"


def add_note(note, filename=NOTES_FILE):
    """Add a note to the specified file."""
    try:
        with open(filename, "a") as f:
            f.write(note + "\n")
        print(f"Note added to {filename}.")
    except Exception as e:
        print(f"Error while adding note: {e}")


def list_notes(filename=NOTES_FILE):
    """List all notes from the specified file."""
    if not os.path.exists(filename):
        print(f"No notes found in {filename}.")
        return
    try:
        with open(filename, "r") as f:
            notes = f.readlines()
        if not notes:
            print(f"No notes in {filename} yet.")
            return
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note.strip()}")
    except Exception as e:
        print(f"Error while reading notes: {e}")


def delete_note(index, filename=NOTES_FILE):
    """Delete a note by index."""
    if not os.path.exists(filename):
        print(f"No notes to delete in {filename}.")
        return
    try:
        with open(filename, "r") as f:
            notes = f.readlines()
        if index < 1 or index > len(notes):
            print(f"Invalid note ID. Please provide a number between 1 and {len(notes)}.")
            return
        deleted = notes.pop(index - 1)
        with open(filename, "w") as f:
            f.writelines(notes)
        print(f"Deleted note: {deleted.strip()}")
    except Exception as e:
        print(f"Error while deleting note: {e}")


def print_usage():
    """Display usage information."""
    print("Usage: qnote [add|list|delete] [note or note_id]")
    print("  add [note]     - Adds a new note")
    print("  list           - Lists all notes")
    print("  delete [id]    - Deletes a note by ID")
    print("  --help         - Displays this message")


def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print_usage()
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a note to add.")
        else:
            note = " ".join(sys.argv[2:])
            add_note(note)
    elif command == "list":
        list_notes()
    elif command == "delete":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Please provide the note number to delete.")
        else:
            delete_note(int(sys.argv[2]))
    else:
        print(f"Unknown command: {command}")
        print_usage()


# Ensure that main is only run when the script is executed directly, not when it's imported
if __name__ == "__main__":
    main()
