import os
import sys
import unittest


# TODO:fix PYTHONPATH so this doesn't have to happen.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import extract.StatsProducer as sp


class TestStatProducer(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(AssertionError):
            sp.StatsProducer(endpoint_name='bad name')

    def test_get_team_stat_data(self):
        stat = sp.StatsProducer(endpoint_name='team stats')


if __name__ == '__main__':
    unittest.main()
