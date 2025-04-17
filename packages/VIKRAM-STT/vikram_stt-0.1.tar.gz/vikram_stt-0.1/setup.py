from setuptools import setup, find_packages

setup(
    name='VIKRAM-STT',
    version='0.1',
    author='Vikram Choure',
    author_email='vikramchoure607@gmail.com',
    description='This is a Speech to Text package created by Vikram Choure',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager'
    ],
)
