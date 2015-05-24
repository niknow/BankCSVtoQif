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


from datetime import datetime
from abc import ABCMeta, abstractmethod


class BankAccountConfig(object):
    """ Abstract class. Stores the configuration data to parse the csv from a specific account.
        For each bank account type, a subclass is implemented. @abstractmethods have to
        be overriden and implemented in the subclass.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.delimiter = None
        self.quotechar = None
        self.dropped_lines = None
        self.default_source_account = None
        self.default_target_account = None

    def normalize_amount(self, amount):
        amount = amount.strip('-')
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if not amount:
            return 0
        return float(amount)

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
        :return: debit of transaction as float
        """
        pass

    @abstractmethod
    def get_credit(self, line):
        """
        :param line: #of csv
        :return: credit of transaction as float
        """
        pass


class DBGiro(BankAccountConfig):
    """ Deutsche Bank Girokonto """

    name = 'db_giro'

    def __init__(self):
        BankAccountConfig.__init__(self)

        self.delimiter = ';'
        self.quotechar = '"'
        self.dropped_lines = 5
        self.default_source_account = 'Assets:Current Assets:Checking Account'
        self.default_target_account = 'Imbalance-EUR'

    def get_date(self, line):
        s = line[0].split('.')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        description = line[2] + ' ' + line[3] + ' ' + line[4]
        return ' '.join(description.split())

    def get_debit(self, line):
        return self.normalize_amount(line[13])

    def get_credit(self, line):
        return self.normalize_amount(line[14])


class DBMaster(BankAccountConfig):
    """ Deutsche Bank Mastercard """

    name = 'db_master'

    def __init__(self):
        BankAccountConfig.__init__(self)
        self.delimiter = ';'
        self.quotechar = '"'
        self.dropped_lines = 5
        self.default_source_account = 'Liabilities:Deutsche Bank Master Card'
        self.default_target_account = 'Imbalance-EUR'

    def get_date(self, line):
        s = line[0].split('.')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        return line[2]

    def get_debit(self, line):
        return self.normalize_amount(line[6])

    def get_credit(self, line):
        return 0


class Lloyds(BankAccountConfig):
    """ Lloyds Checking Account """

    name = 'lloyds'

    def __init__(self):
        BankAccountConfig.__init__(self)
        self.delimiter = ','
        self.quotechar = '"'
        self.dropped_lines = 1
        self.default_source_account = 'Assets:Current Assets:Checking Account'
        self.default_target_account = 'Imbalance-GBP'

    def get_date(self, line):
        s = line[0].split('/')
        return datetime(int(s[2]), int(s[1]), int(s[0]))

    def get_description(self, line):
        return line[4]

    def get_debit(self, line):
        return float(line[5]) if line[5] else 0

    def get_credit(self, line):
        return float(line[6]) if line[6] else 0
