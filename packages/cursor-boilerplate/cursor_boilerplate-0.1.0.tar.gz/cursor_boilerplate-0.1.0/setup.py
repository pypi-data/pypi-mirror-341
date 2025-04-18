from setuptools import setup, find_packages

setup(
    name="cursor-boilerplate",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "uvx=cursor_boilerplate.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A boilerplate project for Cursor IDE",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cursor-boilerplate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 