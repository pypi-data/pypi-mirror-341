
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-python",
    version="0.1.4",
    description="MCP server providing a Python REPL with persistent session",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['llm-parser-filter', 'mcp', 'mcp-gsuite', 'python-dotenv'],
    keywords=["mseep"] + ['mcp', 'repl', 'python', 'server'],
)
