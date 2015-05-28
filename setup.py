# -*- coding: utf-8 -*-


# BankCSVtoQif - Smart conversion of csv files from a bank to qif
# Copyright (C) 2015  Nikolai Nowaczyk
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


from setuptools import setup, find_packages

version = "0.0.1"

setup(
    name='bankcsvtoqif',
    version=version,
    description='Smart conversion of csv files from a bank to qif',
    author='Nikolai Nowaczyk',
    author_email='mail@nikno.de',
    license='GNU GPLv2',
    url='https://github.com/niknow/BankCSVtoQif/tree/master/bankcsvtoqif',
    packages=find_packages(),
    tests_require=['pytest'],
    install_requires=['monthdelta']
)
