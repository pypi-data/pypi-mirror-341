from gtts import gTTS
import os

class ParsTalk:
    def __init__(self):
        print("[ParsTalk] کتابخانه بارگذاری شد!")

    def say(self, text: str, filename: str = "output.mp3"):
        print(f"[ParsTalk] تبدیل متن به صدا: {filename}")
        
        # تبدیل متن به صدا با استفاده از gTTS
        tts = gTTS(text, lang='fa')
        tts.save(filename)
        
        # پخش صدا
        os.system(f"start {filename}")  # برای ویندوز
        # برای سیستم‌عامل‌های دیگر می‌توان از دستورهای زیر استفاده کرد:
        # os.system(f"mpg321 {filename}")  # برای لینوکس
        # os.system(f"afplay {filename}")  # برای مک
