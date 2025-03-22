from setuptools import setup, find_packages

setup(
    name="currency_converter_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'python-dotenv',
        'requests',
    ],
) 