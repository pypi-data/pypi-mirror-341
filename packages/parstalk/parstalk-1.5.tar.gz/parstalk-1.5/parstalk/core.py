import pyttsx3

# تابع برای تبدیل متن فارسی به فینگلیش با در نظر گرفتن مصوت‌ها
def farsi_to_finglish_with_vowels(text):
    vowels = "اایوو"
    farsi_to_finglish_dict = {
        "ا": "a", "ب": "b", "پ": "p", "ت": "t", "ث": "s", "ج": "j", "چ": "ch", "ح": "h", 
        "خ": "kh", "د": "d", "ذ": "z", "ر": "r", "ز": "z", "ژ": "zh", "س": "s", "ش": "sh", 
        "ص": "s", "ض": "z", "ط": "t", "ظ": "z", "ع": "a", "غ": "gh", "ف": "f", "ق": "q", 
        "ک": "k", "گ": "g", "ل": "l", "م": "m", "ن": "n", "و": "v", "ه": "h", "ی": "i"
    }
    
    result = []
    previous_char_was_vowel = False  # Flag to check if the previous character was a vowel

    for char in text:
        if char in farsi_to_finglish_dict:
            # تبدیل حروف فارسی به فینگلیش
            converted_char = farsi_to_finglish_dict[char]

            # اگر قبل از حرفی که مصوت است مصوت نباشد، حرف مصوت شود
            if char in vowels and previous_char_was_vowel:
                result.append(converted_char)  # اضافه کردن حرف مصوت به لیست نتیجه
            elif char in vowels:
                result.append(converted_char)  # اضافه کردن حرف مصوت به لیست نتیجه
                previous_char_was_vowel = True  # تنظیم وضعیت که این حرف مصوت بود
            else:
                result.append(converted_char)  # اگر حرف مصوت نباشد، به سادگی اضافه کن

        else:
            result.append(char)  # اگر حرف در دیکشنری نیست، همان را اضافه کن

    # تبدیل لیست به رشته نهایی
    return "".join(result)

# تابع برای تبدیل به صدا با استفاده از pyttsx3
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
