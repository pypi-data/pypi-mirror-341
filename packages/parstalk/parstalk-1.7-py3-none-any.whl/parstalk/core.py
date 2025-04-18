import pyttsx3

# حروف مصوت و حرکات
vowels = "اآوییو"
harakats_map = {
    '\u064E': 'a',   # َ فتحه
    '\u0650': 'e',   # ِ کسره
    '\u064F': 'o',   # ُ ضمه
    '\u0652': '',    # ْ سکون
    '\u064B': 'an',  # ً تنوین فتح
    '\u064D': 'en',  # ٍ تنوین جر
    '\u064C': 'on',  # ٌ تنوین ضم
}

# جدول تبدیل حرف به فینگلیش
farsi_to_finglish_dict = {
    "آ": "aa", "ا": "a", "ب": "b", "پ": "p", "ت": "t", "ث": "s", "ج": "j",
    "چ": "ch", "ح": "h", "خ": "kh", "د": "d", "ذ": "z", "ر": "r", "ز": "z",
    "ژ": "zh", "س": "s", "ش": "sh", "ص": "s", "ض": "z", "ط": "t", "ظ": "z",
    "ع": "a", "غ": "gh", "ف": "f", "ق": "gh", "ک": "k", "گ": "g", "ل": "l",
    "م": "m", "ن": "n", "و": "v", "ه": "h", "ی": "i", " ": " ", "؟": "?", "!": "!", ".": "."
}

# تابع تبدیل فارسی با حرکات به فینگلیش
def farsi_with_harakats_to_finglish(text):
    result = []
    i = 0

    while i < len(text):
        char = text[i]

        if char in farsi_to_finglish_dict:
            base = farsi_to_finglish_dict[char]
            harakat = ""

            # بررسی اینکه بعد از حرف، حرکت هست یا نه
            if i + 1 < len(text) and text[i + 1] in harakats_map:
                harakat = harakats_map[text[i + 1]]
                i += 1  # پرش از حرکت

            result.append(base + harakat)

        elif char in harakats_map:
            # حرکت‌هایی که به اشتباه تنها وارد شدن
            result.append(harakats_map[char])
        else:
            result.append(char)

        i += 1

    return ''.join(result)

# تبدیل به صدا
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

