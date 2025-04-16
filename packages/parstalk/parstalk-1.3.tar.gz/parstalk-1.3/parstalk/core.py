import pyttsx3

finglish_dict = {
    "آ": "Aa", "ا": "a", "ب": "b", "پ": "p", "ت": "t", "ث": "s", "ج": "j", "چ": "ch", "ح": "h", "خ": "kh", 
    "د": "d", "ذ": "z", "ر": "r", "ز": "z", "ژ": "zh", "س": "s", "ش": "sh", "ص": "s", "ض": "z", 
    "ط": "t", "ظ": "z", "ع": "a", "غ": "gh", "ف": "f", "ق": "gh", "ک": "k", "گ": "g", "ل": "l", 
    "م": "m", "ن": "n", "و": "v", "ه": "h", "ی": "y"
}

vowels = ['ا', 'و', 'ی','آ', 'و']

def farsi_to_finglish_with_vowels(text):
    result = ""
    prev_char = ""
    for char in text:
        if char in finglish_dict:
            if prev_char in vowels and char in vowels:
                result += finglish_dict[char]
            else:
                result += finglish_dict.get(char, char)
        elif char == "َ":
            result += "a"
        elif char == "ُ":
            result += "o"
        elif char == "ِ":
            result += "e"
        elif char == "ْ":
            result += ""
        else:
            result += char
        prev_char = char
    return result
