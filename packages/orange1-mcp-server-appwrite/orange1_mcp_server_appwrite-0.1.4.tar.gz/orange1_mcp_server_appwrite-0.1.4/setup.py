
from setuptools import setup, find_packages

setup(
    name="orange1-mcp-server-appwrite",
    version="0.1.4",
    description="MCP (Model Context Protocol) server for Appwrite",
    author="orange1",
    author_email="support@orange.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['appwrite>=9.0.3', 'docstring-parser>=0.16', 'mcp[cli]>=1.3.0'],
    keywords=["orange1"] + [],
)
