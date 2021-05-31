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

    def test_get_endpoint_url(self):
        stats = sp.StatsProducer(endpoint_name='team')

        url = stats.endpoint

        self.assertEqual(url, sp.AVS_TEAM['endpoint'])

    def test_get_team_stat_data(self):
        stats = sp.StatsProducer(endpoint_name='team stats')

        formatted_dict = stats.get_team_stat_data()

        self.assertTrue(isinstance(formatted_dict['points_pct'], float))
        self.assertTrue(isinstance(formatted_dict['power_play_pct'], float))
        self.assertTrue(isinstance(formatted_dict['penalty_kill_pct'], float))
        self.assertTrue(isinstance(formatted_dict['faceoffs_win_pct'], float))


if __name__ == '__main__':
    unittest.main()
