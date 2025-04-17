
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-alchemy",
    version="2025.04.16.110003",
    description="A MCP server that connects to your database",
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
    install_requires=['mcp[cli]>=1.2.0rc1', 'sqlalchemy>=2.0.36'],
    keywords=["mseep"] + [],
)
