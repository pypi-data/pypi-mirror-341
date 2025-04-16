from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jumpad-sdk-client",
    version="0.1.1",
    author="Jumpad AI",
    author_email="info@jumpad.ai",
    description="A powerful and user-friendly Python client for interacting with the Jumpad AI Agent SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jumpad-ai/jumpad-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
) 