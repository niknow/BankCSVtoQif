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

# This configures parsing of db_giro. Do not touch unless you know what you are doing.
class DBGiroParserFunctions(BankAccountParserFunctions):
    """ Implements a method that gets as an input a line of csv of this bank and returns the
        desired quantity, i.e. date, description, debit, credit """

    @staticmethod
    def line_to_date(line):
        s = line[0].split('.')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    @staticmethod
    def line_to_description(line):
        return line[2]

    @staticmethod
    def line_to_debit(line):
        return BankAccountParserFunctions.normalize_amount(line[6])

    @staticmethod
    def line_to_credit(line):
        return 0


# optional: configure replacements (see Replacement class for documentation)
replacements = []
# replacements = [
#    Replacement('cryptic number 12345', 'Rent', 'Expenses:Flat:Rent', 1),
#]

# configures db_giro account
db_master = BankAccountConfig()
db_master.name = 'db_giro'
db_master.delimiter = ';'
db_master.quotechar = '"'
db_master.dropped_lines = 5
db_master.source_account = 'Liabilities:Deutsche Bank Master Card'
db_master.parser_functions = DBGiroParserFunctions
db_master.replacements = replacements

# parse arguments
parser = argparse.ArgumentParser(description='Smart conversion of csv files from db_master to qif.')
parser.add_argument("csv_file", help="csv file you want to convert")
parser.add_argument("qif_file", nargs='?', default='', help="name of qif file output")
args = parser.parse_args()

if args.qif_file:
    qfile = args.qif_file
else:
    qfile = args.csv_file[:-3]+'qif'

# run conversion and print result
data_manager = DataManager(args.csv_file, qfile, db_master)
data_manager.csv_to_qif()
for transaction in data_manager.transactions:
    print transaction





