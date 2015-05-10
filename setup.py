# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = "0.0.1"

setup(
    name='bankcsvtoqif',
    version=version,
    description='Smart conversion of csv files from a bank to qif',
    author='Nikolai Nowaczyk',
    author_email='mail@nikno.de',
    license='GNU GPLv2',
    url='https://github.com/niknow/BankCSVtoQif',
    packages=find_packages(),
    install_requires=['monthdelta']
)