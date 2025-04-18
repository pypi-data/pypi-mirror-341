from setuptools import setup, find_packages

setup(
    name="parstalk",
    version="1.5",
    description="تبدیل متن فارسی به فینگلیش با تشخیص مصوت و تبدیل به صدا",
    author="Mohammadjavad Ghaderi",
    author_email="Mohammadjavadd.ronaldo@gmail.com",
    packages=find_packages(),
    install_requires=["pyttsx3"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
