#!/usr/bin/python

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

from bankcsvtoqif.bankcsv import DataManager, BankAccountConfig
import bankcsvtoqif.banks
import argparse
import inspect

# create a dictionary of all banks
banks = {}
for name, obj in inspect.getmembers(bankcsvtoqif.banks):
    if inspect.isclass(obj) and issubclass(obj, BankAccountConfig) and not obj is BankAccountConfig:
        banks[obj.name] = obj

# parse arguments
parser = argparse.ArgumentParser(
    description="Smart conversion of csv files from bank statements to qif.",
    epilog="Exampe: python b2q.py db_giro statement_june_15.csv"
)
parser.add_argument('type', choices=banks.keys(), help="account type from which you want to convert")
parser.add_argument('csv_file', help="csv file you want to convert")
parser.add_argument('qif_file', nargs='?', default='', help="name of qif file output")
parser.add_argument('source_account', nargs='?', help="source account, e.g. Assets:Current Assets:Checking Account")
parser.add_argument('target_account', nargs='?', help="default target account, e.g. Imbalance-EUR")
parser.add_argument(
    '-r', '--replacements',
    nargs='?',
    const='replacements.ini',
    help="config file for automatic replacements")
parser.add_argument('-v', action='store_true', help="produce output during conversion")
args = parser.parse_args()


# configure account according to arguments
account_config = banks[args.type]()
qfile = args.qif_file if args.qif_file else args.csv_file[:-3] + 'qif'

# run conversion and print result
data_manager = DataManager(
    args.csv_file,
    qfile,
    args.replacements,
    account_config,
    args.v
)
data_manager.csv_to_qif()
