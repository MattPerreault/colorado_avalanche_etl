import os
import sys
import unittest


# TODO:fix PYTHONPATH so this doesn't have to happen.
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import extract.StatsProducer as sp


class TestStatProducer(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(AssertionError):
            sp.StatsProducer(endpoint_name="bad name")

    def test_get_endpoint_url(self):
        stats = sp.StatsProducer(endpoint_name="team")

        url = stats.endpoint

        self.assertEqual(url, sp.AVS_TEAM["endpoint"])

    def test_get_team_stat_data(self):
        stats = sp.StatsProducer(endpoint_name="team stats")

        formatted_dict = stats.get_team_stat_data()

        self.assertTrue(isinstance(formatted_dict["points_pct"], float))
        self.assertTrue(isinstance(formatted_dict["power_play_pct"], float))
        self.assertTrue(isinstance(formatted_dict["penalty_kill_pct"], float))
        self.assertTrue(isinstance(formatted_dict["faceoffs_win_pct"], float))

    def test_get_roster_data(self):
        stats = sp.StatsProducer(endpoint_name="roster")

        roster_list = stats.get_roster_data()

        self.assertTrue(isinstance(roster_list[0]["player_id"], int))
        self.assertTrue(isinstance(roster_list[0]["jersey_number"], int))

    def test_get_all_player_ids(self):
        stats = sp.StatsProducer(endpoint_name="player_stats_single_season_reg")
        player_id = stats._get_player_ids()
        self.assertTrue(isinstance(player_id, list))

    def test_get_raw_data(self):
        # TODO: Finish test after figuring out how what should be returned.
        simple_stat = sp.StatsProducer(endpoint_name="team")
        expected = {}


if __name__ == "__main__":
    unittest.main()
