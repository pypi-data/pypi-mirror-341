from setuptools import setup, find_packages

setup(
    name="parstalk",
    version="1.3",
    packages=find_packages(),
    install_requires=["pyttsx3"],
    author="Mohammadjavad Ghaderi",
    author_email="Mohammadjavadd.ronaldo@gmail.com",
    description="Convert Farsi text to finglish with vowel detection and play sound",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
