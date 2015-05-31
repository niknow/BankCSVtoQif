# -*- coding: utf-8 -*-
import csv
import unittest

from ..banks import DBGiro, VRBank
from ..transaction import Transaction, TransactionFactory
from datetime import datetime


class BankCSVtoQifTest(unittest.TestCase):
    db_giro_csv1 = """22.04.2015;22.04.2015;"SEPA-Überweisung an";\
        Smith, John;Rent;DE12345678909876543212;\
        BYLADEM1GLA;;;;;;;-10,00;;EUR"""

    # --- test setup and tear down ---
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --- helper functions ---

    def csvline_to_line(self, csvline, account_config):
        csvline = csvline.splitlines()
        csv.register_dialect(
            account_config.name,
            delimiter=account_config.delimiter,
            quotechar=account_config.quotechar
        )
        c = csv.reader(csvline, account_config.name)
        return next(c)

    # --- tests ---

    # banks.py

    def test_db_giro(self):
        account_config = DBGiro()
        line = self.csvline_to_line(BankCSVtoQifTest.db_giro_csv1, account_config)
        date = datetime(2015, 4, 22)
        description = 'SEPA-Überweisung an Smith, John Rent'
        debit = 10
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    # class Transaction
    def test_create_transaction(self):
        date = datetime(2015, 5, 17)
        description = 'milk'
        debit = 1.05
        credit = 0
        account = 'Expenses:Groceries'
        transaction = Transaction(date, description, debit, credit, account)
        self.assertEqual(transaction.date, date)
        self.assertEqual(transaction.description, description)
        self.assertEqual(transaction.debit, debit)
        self.assertEqual(transaction.credit, credit)
        self.assertEqual(transaction.account, account)
        self.assertEqual(transaction.amount, credit - debit)

    def test_transaction_factory(self):
        account_config = DBGiro()
        line = self.csvline_to_line(BankCSVtoQifTest.db_giro_csv1, account_config)
        transaction_factory = TransactionFactory(account_config)
        transaction = transaction_factory.create_from_line(line)
        self.assertEqual(transaction.date, account_config.get_date(line))
        self.assertEqual(transaction.description, account_config.get_description(line))
        self.assertEqual(transaction.debit, account_config.get_debit(line))
        self.assertEqual(transaction.credit, account_config.get_credit(line))
        self.assertEqual(transaction.account, account_config.default_target_account)


class TestVRBank(unittest.TestCase):
    def setUp(self):
        self.d = VRBank()

    def test_can_instanciate(self):
        pass

    def test_extract_correct_fields(self):
        transaction = (TransactionFactory(self.d)).create_from_line(self.get_fixture_line())

        self.assertIsNotNone(transaction.date)
        self.assertEqual('2015-05-22T00:00:00', transaction.date.isoformat())

        self.assertGreater(transaction.debit, 0)
        self.assertGreater(transaction.debit, 8.2)
        self.assertLess(transaction.debit, 9)
        self.assertEqual(transaction.credit, 0)

        print transaction.description
        self.assertTrue('AMAZON' in transaction.description)
        self.assertTrue('32132131321' in transaction.description)
        self.assertTrue('-8,21' not in transaction.description)

    def get_fixture_line(self):
        return [
            '1234456789', '22.05.2015', '22.05.2015', 'AMAZON SERVICES EUROPE S.A.R.L.', 'SEPA-Basislastschrift',
            '101-1234567-8910111 Amazon', 'Services Europe SARL 112233', '32132131321', '556465464564', '', '', '',
            '', '', '', '', '', '', '', '-8,21', '138,69', 'EUR'
        ]
