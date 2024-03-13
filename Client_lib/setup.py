from setuptools import setup, find_packages
# Setting up
setup(
    name="devrevthirtyone",
    version="4.0.0",
    author="team31",
    packages=find_packages(),
    install_requires=['numpy', 'litellm', 'tiktoken'],
)