
from setuptools import setup, find_packages

setup(
    name="orange1-mcp-server-weaviate",
    version="0.1.0",
    description="Add your description here",
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
    install_requires=['weaviate-client==4.10.4'],
    keywords=["orange1"] + [],
)
