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

def reverse(text, line=True):
    """
    Returns a mirrored version of the text.

    Args:
        text (str): Input text to mirror.
        line (bool): If True, adds a "|" separator between original and mirrored version.

    Returns:
        str: Mirrored text.

    Examples:
        mirror_text("abc")       ➜ "abc|cba"
        mirror_text("abc", False) ➜ "cba"
    """
    if line: return str(text) + "|" +  str(text)[::-1]
    return str(text)[::-1]

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
    
    Raises:
        ValueError: If a number is invalid for the given base or the base itself is unsupported.
    """
    if base != 0 and (base < 2 or base > 36):
        raise ValueError("base must be >= 2 and <= 36, or 0")
    string = ""
    for number in numbers:
        try:
            string += chr(int(number, base))
        except ValueError:
            raise ValueError(f"{number} not in base: {base}, base ranges from 0 to {base-1}")
    return string
def to_snake_case(text):
    """
    Converts a string to snake_case without using regex.
    Handles camelCase, PascalCase, spaces and hyphens.
    """
    result = []
    for i, char in enumerate(text):
        if char.isupper():
            if i > 0 and (text[i-1].islower() or text[i-1].isdigit()):
                result.append('_')
            result.append(char.lower())
        elif char in {' ', '-'}:
            result.append('_')
        else:
            result.append(char)
    return ''.join(result)
def to_camel_case(text):
    """
    Converts a string to camelCase without using regex.
    Accepts snake_case, kebab-case and space-separated strings.
    """
    parts = []
    current = ''
    for char in text:
        if char in {'_', '-', ' '}:
            if current:
                parts.append(current)
                current = ''
        else:
            current += char
    if current:
        parts.append(current)

    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
def to_1337(text):
    """
    Converts text to the famous 1337 style.
    """
    replacements = {'a': '@', 'e': '3', 'i': '!', 'l': '1', 'o': '0', 't': '7', 's': '5', 'z': '2'}
    return ''.join(replacements.get(c.lower(), c) for c in text)
    