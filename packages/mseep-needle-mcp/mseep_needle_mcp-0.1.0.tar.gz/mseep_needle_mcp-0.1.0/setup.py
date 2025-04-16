
from setuptools import setup, find_packages

setup(
    name="mseep-needle-mcp",
    version="0.1.0",
    description="Needle MCP integration",
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
    install_requires=['needle-python>=0.4.0', 'mcp>=1.1.0', 'python-dotenv>=1.0.1'],
    keywords=["mseep"] + [],
)
