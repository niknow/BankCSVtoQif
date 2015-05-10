# -*- coding: utf-8 -*-

from bankcsvtoqif.bankcsv import DataManager, BankAccountConfig, BankAccountParserFunctions
from bankcsvtoqif.smartlabeler import Replacement
from datetime import datetime


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
        description = line[2] + ' ' + line[3] + ' ' + line[4]
        return ' '.join(description.split())

    @staticmethod
    def line_to_debit(line):
        return BankAccountParserFunctions.normalize_amount(line[13])

    @staticmethod
    def line_to_credit(line):
        return BankAccountParserFunctions.normalize_amount(line[14])


# optional: configure replacements (see Replacement class for documentation)
replacements = []
#replacements = [
#    Replacement('cryptic number 12345', 'Rent', 'Expenses:Flat:Rent', 1),
#]

# configures db_giro account
db_giro = BankAccountConfig()
db_giro.name = 'db_giro'
db_giro.delimiter = ';'
db_giro.quotechar = '"'
db_giro.dropped_lines = 5
db_giro.source_account = 'Assets:Current Assets:Checking Account'
db_giro.parser_functions = DBGiroParserFunctions
db_giro.replacements = replacements

# run conversion and print result
data_manager = DataManager('raw_csv_from_bank.csv',
                           'converted_qif_file.qif',
                           db_giro)
data_manager.csv_to_qif()
for transaction in data_manager.transactions:
    print transaction
