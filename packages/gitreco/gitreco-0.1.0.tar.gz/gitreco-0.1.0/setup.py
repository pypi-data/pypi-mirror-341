# setup.py
from setuptools import setup, find_packages

setup(
    name="gitreco",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ollama",  # 필요한 외부 패키지
    ],
    entry_points={
        "console_scripts": [
            "gitreco=gitreco.cli:main",
        ],
    },
    python_requires=">=3.7",
)
