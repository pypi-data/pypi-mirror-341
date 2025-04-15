from setuptools import setup, find_packages

setup(
    name="kwasa-cli",
    version="1.0.1",
    description="Simple CLI tool for cloning and updating the repository",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jeckonia Kwasa",
    author_email="aurinkowebner@gmail.com",
    url="https://github.com/jeckonia49/kwasa-cli",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.1.0",
        "requests>=2.32.3",
        "colored>=2.3.0",
    ],
    extras_require={
        "dev": [
            "mypy>=1.15.0",
            "pytest-cov>=6.1.1",
            "pytest>=8.3.5",
            "ruff>=0.11.4",
            "pre-commit>=4.2.0",
            "setuptools>=78.1.0",
            "build>=1.2.2.post1",
            "hatch>=1.14.0",
            "twine>=6.1.0",
        ],
    },
    entry_points={"console_scripts": ["kwasa = kwasa.main:main"]},
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
    ],
)
