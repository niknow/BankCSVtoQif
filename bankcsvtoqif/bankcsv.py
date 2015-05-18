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


import collections
from itertools import islice
import csv
from bankcsvtoqif import qif
from bankcsvtoqif.smartlabeler import SmartLabeler


def consume(iterator, n):
    """Advance the iterator n-steps ahead. If n is none, consume entirely."""
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


class Transaction(object):
    """ Represents a transaction obtained from csv-file. """

    def __init__(self, date, description, debit, credit, account):
        self.date = date
        self.description = description
        self.debit = debit
        self.credit = credit
        self.account = account

    def __str__(self):
        return '<Transaction %s, %s, %s, %s, %s>' % (self.date, self.description, self.debit, self.credit, self.account)

    @property
    def amount(self):
        return self.credit - self.debit


class BankAccountConfig(object):
    """ Abstract class. Stores the configuration data to parse the csv from a specific account.
        For each bank account type, a subclass is implemented in banks.py. All parse_-methods have to
        be overriden and implemented in the subclass.
    """

    def __init__(self):
        self.delimiter = None
        self.quotechar = None
        self.dropped_lines = None
        self.source_account = None
        self.target_account = None
        self.parser_functions = None

    @staticmethod
    def normalize_amount(amount):
        amount = amount.strip('-')
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        if not amount:
            return 0
        return float(amount)

    @staticmethod
    def parse_line_to_date(line):
        """
        :param line: #of csv
        :return:  date of transaction as datetime
        """
        pass

    @staticmethod
    def parse_line_to_description(line):
        """
        :param line: #of csv
        :return: description of transaction as string
        """
        pass

    @staticmethod
    def parse_line_to_debit(line):
        """
        :param line: #of csv
        :return: debit of transaction as float
        """
        pass

    @staticmethod
    def parse_line_to_credit(line):
        """
        :param line: #of csv
        :return: credit of transaction as float
        """
        pass


class Messenger(object):
    """ Handles console output.  """

    def __init__(self, on):
        self.on = on

    @staticmethod
    def newlines(num):
        if num:
            print("\n" * (num - 1))

    def send_message(self, msg):
        if self.on:
            print(msg)


class DataManager(object):
    """ Main class to interact with the user. """

    def __init__(self, csv_filename, qif_filename, replacements_file, account_config, verbose):
        self.csv_filename = csv_filename
        self.qif_filename = qif_filename
        self.replacements_file = replacements_file
        self.account_config = account_config
        self.messenger = Messenger(verbose)
        self.transactions = []

    def read_csv(self):
        self.messenger.send_message("\nParsing csv-file from" + self.csv_filename + "...")
        f = open(self.csv_filename, 'rt')
        csv.register_dialect(self.account_config.name,
                             delimiter=self.account_config.delimiter,
                             quotechar=self.account_config.quotechar)
        c = csv.reader(f, self.account_config.name)
        consume(c, self.account_config.dropped_lines)  # ignore first lines
        for line in c:
            try:
                par_fun = self.account_config
                transaction = Transaction(par_fun.parse_line_to_date(line),
                                          par_fun.parse_line_to_description(line),
                                          par_fun.parse_line_to_debit(line),
                                          par_fun.parse_line_to_credit(line),
                                          self.account_config.target_account)
                self.transactions.append(transaction)
                self.messenger.send_message("parsed: " + transaction.__str__())
            except IndexError:
                self.messenger.send_message('skipped: %s' % line)
                continue
        f.close()

    def relabel_transactions(self):
        self.messenger.send_message("\nConducting automatic replacements using " + self.replacements_file + "...")
        if self.replacements_file:
            smart_labeler = SmartLabeler()
            smart_labeler.load_replacements_from_file(self.replacements_file, self.account_config.name)
            for index, transaction in enumerate(self.transactions):
                replacement = smart_labeler.has_replacement(transaction)
                if replacement:
                    self.transactions[index] = smart_labeler.replace(transaction, replacement)
                    self.messenger.send_message("replaced: " + self.transactions[index].__str__())

    def write_qif(self):
        self.messenger.send_message("\nWriting qif-file to " + self.qif_filename + "...")
        q = qif.Qif(self.account_config.source_account)
        for transaction in self.transactions:
            q.add_transaction(
                qif.Transaction(transaction.date, transaction.account, transaction.description, transaction.amount))
        q.save(self.qif_filename)

    def print_transactions(self):
        self.messenger.send_message("\nFinished! Qif contains the following transactions:")
        for transaction in self.transactions:
            self.messenger.send_message(transaction)

    def csv_to_qif(self):
        self.read_csv()
        self.relabel_transactions()
        self.write_qif()
        self.print_transactions()
