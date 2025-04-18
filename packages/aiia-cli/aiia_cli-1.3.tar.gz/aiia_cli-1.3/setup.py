from setuptools import setup

setup(
    name="aiia-cli",
    version="1.3",
    py_modules=["cli"],
    install_requires=["click"],
    entry_points={"console_scripts": ["proj-cli=cli:cli"]}
)