"""核对原始业务资料之间的引用与记录形式。"""

import unittest

from inspect_samples import read_samples


class SampleTests(unittest.TestCase):
    def setUp(self):
        self.data = read_samples()

    def test_substitution_refers_to_a_sale(self):
        observations = self.data['observations']
        sales = {(row['day'], row['item'], row['minute']): row['amount'] for row in observations if row['event'] == '领取'}
        links = [row for row in observations if row['event'] == '替代领餐']
        empty = {(row['day'], row['item']) for row in observations if row['event'] == '核余' and row['amount'] == 0}
        self.assertTrue(links)
        for link in links:
            self.assertLessEqual(link['amount'], sales[link['day'], link['substitute'], link['linked_minute']])
            self.assertIn((link['day'], link['item']), empty)

    def test_service_has_stockout_and_restock_records(self):
        observations = self.data['observations']
        missing = {(row['day'], row['item']) for row in observations if row['event'] == '核余' and row['amount'] == 0}
        stocked = {(row['day'], row['item']) for row in observations if row['event'] == '补货'}
        self.assertTrue(missing & stocked)
        self.assertTrue(any(row['received'] > row['minute'] for row in observations))
