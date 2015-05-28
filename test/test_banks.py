# -*- coding: utf-8 -*-
import unittest
from bankcsvtoqif.banks import VRBank
from bankcsvtoqif.transaction import TransactionFactory


class TestBanks(unittest.TestCase):
    def setUp(self):
        self.d = VRBank()

    def test_can_instanciate(self):
        pass

    def test_extract_correct_fields(self):
        transaction = (TransactionFactory(self.d)).create_from_line(self.get_fixture_line())

        self.assertIsNotNone(transaction.date)
        self.assertEqual('2015-05-22T00:00:00', transaction.date.isoformat())

        self.assertLess(transaction.credit, 0)
        self.assertLess(transaction.credit, -8.2)
        self.assertGreater(transaction.credit, -9)
        self.assertEqual(transaction.debit, 0)

        self.assertTrue('AMAZON' in transaction.description)
        self.assertTrue('32132131321' in transaction.description)

    def get_fixture_line(self):
        return [
            '1234456789', '22.05.2015', '22.05.2015', 'AMAZON SERVICES EUROPE S.A.R.L.', 'SEPA-Basislastschrift',
            '101-1234567-8910111 Amazon', 'Services Europe SARL 112233', '32132131321', '556465464564', '', '', '',
            '', '', '', '', '', '', '', '-8,21', '138,69', 'EUR'
        ]


if __name__ == '__main__':
    unittest.main()
