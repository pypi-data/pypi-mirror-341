
from setuptools import setup, find_packages

setup(
    name="mseep-create-mcp-server",
    version="1.0.6.dev0",
    description="Create an Model Context Protocol server project from a template.",
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
    install_requires=['click>=8.1.7', 'jinja2>=3.1.4', 'packaging>=24.2', 'toml>=0.10.2'],
    keywords=["mseep"] + [],
)
