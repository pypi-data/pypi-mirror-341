from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="sistme_bancario",
    version="0.0.1",
    author="Raphael",
    author_email="pererap015@gmail.com",
    description="Sistema bancário com python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raphael2203/diostudy/blob/main/sistema_bancario2.py",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)