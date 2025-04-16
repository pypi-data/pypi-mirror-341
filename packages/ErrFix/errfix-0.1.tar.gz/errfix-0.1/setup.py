from setuptools import setup, find_packages

setup(
    name="ErrFix",
    version="0.1",
    author="Twoje Imię",
    author_email="twojemail@example.com",
    description="Pakiet do diagnozowania i weryfikacji błędów w Pythonie",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)