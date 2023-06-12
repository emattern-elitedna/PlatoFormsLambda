import string
from nameparser import HumanName


def clean_string(input_string):
    # Removes all characters that are not ascii letters or digits, or a space
    allowed_characters = string.ascii_letters + string.digits + ' ' + ','
    cleaned_string = ''.join(char for char in input_string if char in allowed_characters)
    return cleaned_string


def parse_name(name):
    # Parses a given name to first and last name
    if name:
        name_cleaned = clean_string(name)
        name = HumanName(name_cleaned)
        return (name.first.title(), name.last.title())
    return None