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


from bankcsvtoqif.qif import QifFile
from bankcsvtoqif.smartlabeler import SmartLabeler
from bankcsvtoqif.transaction import TransactionFactory


class Messenger(object):
    """ Handles console output.  """

    def __init__(self, on):
        self.on = on

    def send_message(self, msg, preblanks=0):
        if self.on:
            for blank in range(0, preblanks):
                print()
            print(msg)


class DataManager(object):
    """ Main class to interact with the user. """

    def __init__(self, account_config, args):

        self.account_config = account_config
        if args.source_account:
            self.account_config.default_source_account = args.source_account
        if args.target_account:
            self.account_config.default_target_account = args.target_account
        self.type = args.type
        self.csv_filename = args.csv_file
        self.qif_filename = args.qif_file if args.qif_file else args.csv_file[:-3] + 'qif'
        self.replacements_file = args.replacements
        self.messenger = Messenger(args.v)
        self.transactions = []

    def read_csv(self, f):
        self.messenger.send_message("Parsing csv-file from" + self.csv_filename + "...", preblanks=1)
        transaction_factory = TransactionFactory(self.account_config)
        self.transactions = transaction_factory.read_from_file(f, self.messenger)

    def relabel_transactions(self, f):
        self.messenger.send_message("Conducting automatic replacements using " + self.replacements_file + "...", preblanks=1)
        smart_labeler = SmartLabeler()
        smart_labeler.load_replacements_from_file(f, self.type)
        smart_labeler.run_replacements(self.transactions, self.messenger)

    def write_qif(self, f):
        self.messenger.send_message("Writing qif-file to " + self.qif_filename + "...", preblanks=1)
        q = QifFile(self.account_config.default_source_account)
        f.write('\n'.join(q.get_raw_data(self.transactions)))

    def print_transactions(self):
        self.messenger.send_message("Finished! Qif contains the following transactions:", preblanks=1)
        for transaction in self.transactions:
            self.messenger.send_message(transaction)

    def csv_to_qif(self):
        f = open(self.csv_filename)
        self.read_csv(f)
        f.close()
        if self.replacements_file:
            f = open(self.replacements_file)
            self.relabel_transactions(f)
            f.close()
        f = open(self.qif_filename, 'w')
        self.write_qif(f)
        f.close()
        self.print_transactions()
