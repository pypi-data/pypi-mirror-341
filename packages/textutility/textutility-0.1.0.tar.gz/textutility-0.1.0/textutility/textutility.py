def is_str(value):
    """
    Returns True if the input is a string-like value.
    Returns False if the input looks like a number or a boolean ("True"/"False").
    """
    if value.title() in ('True', 'False'):
        return False
    elif value.lstrip('-').isdigit():
        return False
    elif value.count('.') == 1 and value.replace('.', '').lstrip('-').isdigit():
        if not value.startswith('.') and not value.endswith('.'):
            return False
    return True

def only_letters(value):
    """
    Returns True if the input contains only alphabetic characters.
    """
    return value.isalpha()

def repeat(value, times):
    """
    Returns the input string repeated `times` times.
    """
    return value * times

def reverse(value):
    """
    Returns the input string reversed.
    """
    return value[::-1]

def count_substring(value, substring):
    """
    Returns the number of times `substring` appears in `value`.
    """
    return value.count(substring)

def no_spaces(value):
    """
    Removes leading and trailing spaces, then replaces all spaces with hyphens.
    """
    return value.strip().replace(' ', '-')

def is_anagram(value1, value2):
    """
    Returns True if both input strings are anagrams of each other.
    """
    return sorted(value1) == sorted(value2)

def longest_prefix(value1, value2):
    """
    Returns the longest common prefix between two strings.
    """
    prefix = ''
    for i in range(min(len(value1), len(value2))):
        if value1[i] == value2[i]:
            prefix += value1[i]
        else:
            break
    return prefix

def reverse_bits(char):
    """
    Returns a character whose ASCII code is the bitwise negation of the input character.
    Works only with single characters (8-bit ASCII).
    """
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError("Please provide a single character!")

    value = ord(char)
    flipped = ~value & 0xFF  # limit to 8-bit range
    return chr(flipped)
def string_from_int(*numbers, base=10):
    """
    Converts a sequence of numbers (as strings or integers) from a given base into a string.

    Args:
        *numbers: Values to decode into characters.
        base (int): The base in which the numbers are represented (e.g., 2, 10, 16).

    Returns:
        str: Decoded string from the given numbers.
    """
    string = ""
    for number in numbers:
        string += chr(int(number, base))
    return string
