from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name = 'willphanpy',
    version = '0.2.0',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "torch",
        "matplotlib",
        "pandas"
    ],
    long_description=description,
    long_description_content_type = "text/markdown"
)