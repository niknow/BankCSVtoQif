# -*- coding: utf-8 -*-


class Qif(object):
    """Interface to .qif-file"""

    def __init__(self, account):
        self.account = account
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def save(self, filename):
        lines = [
            '!Account',
            'N' + self.account,
            '^'
        ]
        for t in self.transactions:
            lines += t.get_lines()

        fp = open(filename, 'w')
        fp.write('\n'.join(lines))
        fp.close()


class Transaction(object):
    """A qif-Transaction"""

    def __init__(self, date, account, description, amount):
        self.date = date
        self.account = account
        self.description = description
        self.amount = amount

    def get_lines(self):
        return [
            '!Type:Cash',
            'D' + self.date.strftime('%m/%d/%y'),
            'S' + self.account,
            'P' + self.description,
            '$' + '%.2f' % self.amount,
            '^'
        ]

