import re


def append_text_to_file(filename, text):
    """Append text to a file."""
    with open(filename, "a") as file:
        file.write(text + "\n")


def is_valid_email(email):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return bool(re.match(pattern, email))
