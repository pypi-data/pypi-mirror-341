# setup.py
from setuptools import setup, find_packages

setup(
    name="pyttsgen",
    version="0.1.0",
    description="A developer-friendly, plug-and-play TTS library for Python supporting multiple outputs and integrations.",
    author="RePromptsQuest",
    author_email="repromptsquest@gmail.com",
    packages=find_packages(),
    install_requires=[
        "edge_tts",
        "streamlit",
        "nest_asyncio"
    ],
    entry_points={
        "console_scripts": [
            "pyttsgen=pyttsgen.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
