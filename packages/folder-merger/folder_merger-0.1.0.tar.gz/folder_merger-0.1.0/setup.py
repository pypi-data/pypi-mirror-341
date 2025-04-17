from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="folder-merger",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility for safely merging multiple folders while handling file conflicts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/folder-merger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tqdm>=4.45.0",
    ],
    entry_points={
        "console_scripts": [
            "folder-merger=folder_merger.cli:main",
        ],
    },
) 