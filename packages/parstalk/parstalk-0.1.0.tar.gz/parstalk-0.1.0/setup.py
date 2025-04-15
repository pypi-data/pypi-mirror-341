
### 8. فایل `parstalk/setup.py`
##این فایل برای نصب و پیکربندی کتابخانه در سیستم‌های مختلف استفاده می‌شود.

#```python
from setuptools import setup, find_packages

setup(
    name="parstalk",
    version="0.1.0",
    description="تبدیل متن فارسی به گفتار با gTTS",
    author="Mohammadjavad Ghaderi",
    author_email="mohammadjavadd.ronaldo@gmail.com",
    packages=find_packages(),
    install_requires=["gTTS"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
