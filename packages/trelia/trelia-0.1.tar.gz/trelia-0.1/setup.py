from setuptools import setup, find_packages

setup(
    name="trelia",
    version="0.1",
    description="A package to rate student code using Gemini API",
    author="Naveen Valluri",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
    ],
    python_requires='>=3.7',
)
