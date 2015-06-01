# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from ..smartlabeler import Replacement


class ReplacementTest(unittest.TestCase):

    def setUp(self):
        self.replacement0 = Replacement('Rent', 'Rent', 'Expenses:Rent', 0)
        self.replacement1 = Replacement('Rent', 'Rent', 'Expenses:Rent', 1)
        self.replacement2 = Replacement('Rent', 'Rent', 'Expenses:Rent', 2)

    def tearDown(self):
        pass


    def test_replacement_matches(self):
        self.assertEqual(self.replacement1.matches('Rent'), True)

    def test_replacement_should_append_date(self):
        self.assertEqual(self.replacement0.should_append_date(), False)
        self.assertEqual(self.replacement1.should_append_date(), True)
        self.assertEqual(self.replacement2.should_append_date(), True)

    def test_replacement_should_append_next_month_date(self):
        self.assertEqual(self.replacement0.should_append_next_month_date(), False)
        self.assertEqual(self.replacement1.should_append_next_month_date(), False)
        self.assertEqual(self.replacement2.should_append_next_month_date(), True)

    def test_replacement_get_description(self):
        date = datetime(2015, 5, 1)
        self.assertEqual(self.replacement0.get_description(date), 'Rent')
        self.assertEqual(self.replacement1.get_description(date), 'Rent 2015-05')
        self.assertEqual(self.replacement2.get_description(date), 'Rent 2015-06')
