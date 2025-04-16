
from setuptools import setup, find_packages

setup(
    name="mseep-logfire-mcp",
    version="None",
    description="The Logfire MCP server! 🔍",
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
    install_requires=['logfire>=3.7.1', 'mcp[cli]>=1.4.1'],
    keywords=["mseep"] + [],
)
