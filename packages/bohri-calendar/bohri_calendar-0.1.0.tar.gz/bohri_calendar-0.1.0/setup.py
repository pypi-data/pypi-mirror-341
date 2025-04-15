from setuptools import setup, find_packages

# Try to read README.md, but don't fail if it's not there
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Bohri Calendar - A tool for generating Bohri calendar PDFs"

setup(
    name="bohri_calendar",
    version="0.1.0",
    author="Yusuf Sabuwala",
    author_email="yusuff.0279@gmail.com",
    description="A tool for generating Bohri calendar PDFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "playwright",
        "Pillow",
        "reportlab",
        "asyncio",
    ],
    entry_points={
        'console_scripts': [
            'bohri-calendar=bohri_calendar.cli:main',
        ],
    },
)