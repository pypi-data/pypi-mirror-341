from setuptools import setup, find_packages

setup(
    name="tUilKit",  # Make sure this name is unique on PyPI
    version="0.1.0",
    author="Daniel Austin",
    author_email="the.potato.gnome@gmail.com",
    description="A toolkit with utility functions for various tasks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yourrepo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
