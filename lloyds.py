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


from bankcsvtoqif.bankcsv import DataManager, BankAccountConfig, BankAccountParserFunctions
from bankcsvtoqif.smartlabeler import Replacement
from datetime import datetime
import argparse


# This configures parsing of lloyds. Do not touch unless you know what you are doing.
class DBGiroParserFunctions(BankAccountParserFunctions):
    """ Implements a method that gets as an input a line of csv of this bank and returns the
        desired quantity, i.e. date, description, debit, credit """

    @staticmethod
    def line_to_date(line):
        s = line[0].split('/')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    @staticmethod
    def line_to_description(line):
        return line[4]

    @staticmethod
    def line_to_debit(line):
        return float(line[5]) if line[5] else 0

    @staticmethod
    def line_to_credit(line):
        return float(line[6]) if line[6] else 0


# optional: configure replacements (see Replacement class for documentation)
replacements = []
# replacements = [
# Replacement('cryptic number 12345', 'Rent', 'Expenses:Flat:Rent', 1),
#]

# configures lloyds account
lloyds = BankAccountConfig()
lloyds.name = 'lloyds'
lloyds.delimiter = ','
lloyds.quotechar = '"'
lloyds.dropped_lines = 1
lloyds.source_account = 'Assets:Current Assets:Checking Account'
lloyds.target_account = 'Imbalance-GBP'
lloyds.parser_functions = DBGiroParserFunctions
lloyds.replacements = replacements

# parse arguments
parser = argparse.ArgumentParser(description='Smart conversion of csv files from lloyds to qif.')
parser.add_argument("csv_file", help="csv file you want to convert")
parser.add_argument("qif_file", nargs='?', default='', help="name of qif file output")
args = parser.parse_args()

if args.qif_file:
    qfile = args.qif_file
else:
    qfile = args.csv_file[:-3] + 'qif'

# run conversion and print result
data_manager = DataManager(args.csv_file, qfile, lloyds)
data_manager.csv_to_qif()
for transaction in data_manager.transactions:
    print transaction
