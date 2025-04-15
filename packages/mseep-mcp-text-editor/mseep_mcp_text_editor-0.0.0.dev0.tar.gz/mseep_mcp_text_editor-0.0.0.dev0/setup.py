
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-text-editor",
    version="None",
    description="MCP Text Editor Server - Edit text files via MCP protocol",
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
    install_requires=['asyncio>=3.4.3', 'mcp>=1.1.2', 'chardet>=5.2.0'],
    keywords=["mseep"] + [],
)
