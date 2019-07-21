import re


def string_to_boolean(string):
    if string == '1':
        return True
    elif string == '0':
        return False
    else:
        return None


def is_numeric(string):
    return not not re.search(r'\d', string)
