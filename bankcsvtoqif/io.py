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
import csv
from itertools import islice
from . import qif
from .smartlabeler import SmartLabeler
from .transaction import TransactionFactory


def consume(iterator, n):
    """Advance the iterator n-steps ahead. If n is none, consume entirely."""
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


class Messenger(object):
    """ Handles console output.  """

    def __init__(self, on):
        self.on = on

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
        csv.register_dialect(
            self.account_config.name,
            delimiter=self.account_config.delimiter,
            quotechar=self.account_config.quotechar
        )
        c = csv.reader(f, self.account_config.name)
        consume(c, self.account_config.dropped_lines)  # ignore first lines
        transaction_factory = TransactionFactory(self.account_config)
        for line in c:
            try:
                transaction = transaction_factory.create_from_line(line)
                self.transactions.append(transaction)
                self.messenger.send_message("parsed: " + transaction.__str__())
            except IndexError:
                self.messenger.send_message('skipped: %s' % line)
                continue
        f.close()

    def relabel_transactions(self):
        if self.replacements_file:
            self.messenger.send_message("\nConducting automatic replacements using " + self.replacements_file + "...")
            smart_labeler = SmartLabeler()
            smart_labeler.load_replacements_from_file(self.replacements_file, self.account_config.name)
            for index, transaction in enumerate(self.transactions):
                replacement = smart_labeler.has_replacement(transaction)
                if replacement:
                    self.transactions[index] = smart_labeler.replace(transaction, replacement)
                    self.messenger.send_message("replaced: " + self.transactions[index].__str__())

    def write_qif(self):
        self.messenger.send_message("\nWriting qif-file to " + self.qif_filename + "...")
        q = qif.Qif(self.account_config.default_source_account)
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
