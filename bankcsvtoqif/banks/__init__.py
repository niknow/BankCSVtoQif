# -*- coding: utf-8 -*-


# BankCSVtoQif - Smart conversion of csv files from a bank to qif
# Copyright (C) 2015-2016  Nikolai Nowaczyk
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

from abc import ABCMeta, abstractmethod
import csv

from bankcsvtoqif.transaction import TransactionType


class BankAccountConfig(object):
    """ Abstract class. Stores the configuration data to parse the csv from a specific account.
        For each bank account type, a subclass is implemented. @abstractmethods have to
        be overriden and implemented in the subclass.
    """

    __metaclass__ = ABCMeta

    transaction_type = TransactionType.CASH

    def __init__(self):
        self.delimiter = None
        self.quotechar = None
        self.dropped_lines = None
        self.default_source_account = None
        self.default_target_account = None

    def get_absolute_amount(self, amount):
        amount = amount.strip('-')
        amount = amount.strip(' ')
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if not amount:
            return 0
        return float(amount)

    def get_amount(self, amount):
        amount = amount.replace(' ', '')
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if not amount:
            return 0
        return float(amount)

    def get_csv_dialect(self):
        d = csv.excel()
        d.delimiter = self.delimiter
        d.quotechar = self.quotechar
        return d

    @abstractmethod
    def get_date(self, line):
        """
        :param line: #of csv
        :return:  date of transaction as datetime
        """
        pass

    @abstractmethod
    def get_description(self, line):
        """
        :param line: #of csv
        :return: description of transaction as string
        """
        pass

    @abstractmethod
    def get_debit(self, line):
        """
        :param line: #of csv
        :return: debit of transaction as a non-negative float
        """
        pass

    @abstractmethod
    def get_credit(self, line):
        """
        :param line: #of csv
        :return: credit of transaction as non-negative float
        """
        pass

    def get_target_account(self, line):
        """
        This function can be overloaded for banks whose csv format
        already contains the target account.
        :param line: #of csv
        :return: target account of a transaction
        """
        return self.default_target_account

    def get_source_account(self, line):
        """
        This function can be overloaded for banks whose csv format
        contains transactions from multiple accounts making it neccessary
        to parse the source account.
        :param line: #of csv
        :return: source account of a transaction
        """
        return self.default_source_account

    def get_transaction_type(self, line):
        """
        This function can be overloaded for banks whose csv format
        contains transactions from multiple accounts, where the accounts
        have different transaction types.
        :param line: #of csv
        :return: transaction type
        """
        return self.transaction_type
