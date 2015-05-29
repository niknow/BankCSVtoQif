# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from ..smartlabeler import Replacement


class ReplacementTest(unittest.TestCase):
    def test_replacement_matches(self):
        replacement = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        self.assertEqual(replacement.matches('Rent'), True)

    def test_replacement_should_append_date(self):
        replacement0 = Replacement('Rent', 'Rent', 'Expenses:Rent', 0)
        replacement1 = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        replacement2 = Replacement('Rent', 'Rent', 'Expenses:Rent', 2)
        self.assertEqual(replacement0.should_append_date(), False)
        self.assertEqual(replacement1.should_append_date(), True)
        self.assertEqual(replacement2.should_append_date(), True)

    def test_replacement_should_append_next_month_date(self):
        replacement0 = Replacement('Rent', 'Rent', 'Expenses:Rent', 0)
        replacement1 = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        replacement2 = Replacement('Rent', 'Rent', 'Expenses:Rent', 2)
        self.assertEqual(replacement0.should_append_next_month_date(), False)
        self.assertEqual(replacement1.should_append_next_month_date(), False)
        self.assertEqual(replacement2.should_append_next_month_date(), True)

    def test_replacement_get_description(self):
        replacement0 = Replacement('RentXYZ', 'Rent', 'Expenses:Rent', 0)
        replacement1 = Replacement('RentXYZ', 'Rent', 'Expenses:Rent', 1)
        replacement2 = Replacement('RentXYZ', 'Rent', 'Expenses:Rent', 2)
        replacement3 = Replacement('RentXYZ', '', 'Expenses:Rent', 2)
        date = datetime(2015, 5, 1)
        self.assertEqual(replacement0.get_description(date), 'Rent')
        self.assertEqual(replacement1.get_description(date), 'Rent 2015-05')
        self.assertEqual(replacement2.get_description(date), 'Rent 2015-06')
        self.assertEqual(replacement3.get_description(date), 'RentXYZ')
