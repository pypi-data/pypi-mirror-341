# setup.py
from setuptools import setup, find_packages

setup(
    name="gitreco",
    version="0.1.1",
    description="Generate commit messages using LLM and git diff",
    author="Jungchan Son",
    author_email="rnrmfjc@gmail.com",
    packages=find_packages(),
    install_requires=[
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "gitreco=gitreco.cli:main",
        ],
    },
    python_requires=">=3.7",
)
