import requests
import psycopg2

from configuration.config import config

AVS_TEAM = {'endpoint': 'https://statsapi.web.nhl.com/api/v1/teams/21',
            'endpoint_name': 'team'}

AVS_TEAM_STATS = {'endpoint': 'https://statsapi.web.nhl.com/api/v1/teams/21/stats',
                  'endpoint_name': 'team stats'}

AVS_ROSTER = {'endpoint': 'https://statsapi.web.nhl.com/api/v1/teams/21/roster',
              'endpoint_name': 'roster'}

AVS_PLAYER_REG_SEASON = {'endpoint': 'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season=20202021',
                         'endpoint_name': 'player_stats_single_season_reg'}

ENDPOINT_NAMES = ['team', 'team stats',
                  'roster', 'player_stats_single_season_reg']

ENDPOINT_LIST = [AVS_TEAM, AVS_TEAM_STATS, AVS_ROSTER, AVS_PLAYER_REG_SEASON]


class StatsProducer:
    """Class that takes in a valid NHL API endpoint name as documented
    in the NHL API documentation github (see README.md) and returns that
    data as a formatted list of dictionaries.
    """
    def __init__(self, endpoint_name=AVS_TEAM['endpoint_name']):
        assert endpoint_name in ENDPOINT_NAMES, "Endpoint name not defined."
        self.raw_data = None
        self.player_ids = []
        self.endpoint = self._get_endpoint_url(endpoint_name)

    def _get_endpoint_url(self, endpoint_name) -> str:
        """Returns the REST endpoint url for the given name."""
        ep_url = None
        for ep_dict in ENDPOINT_LIST:
            if ep_dict['endpoint_name'] == endpoint_name:
                ep_url = ep_dict['endpoint']
        return ep_url

    def _get_raw_data(self) -> dict:
        """Returns a JSON encoded dict list of raw data."""
        try:
            self.raw_data = requests.get(self.endpoint)
            self.raw_data.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return self.raw_data.json()

    def _get_player_ids(self) -> list:
        """Returns a list of player_id's from the active roster
        to be used for making API request"""
        player_ids = []
        sql = 'SELECT player_id FROM roster'
        db_creds = config()
        try:
            print('Connecting to the db...')
            conn = psycopg2.connect(**db_creds)
            cur = conn.cursor()
            print('Running SELECT statement to get all player_ids...')
            cur.execute(sql)

            raw_data = cur.fetchall()
            for row in raw_data:
                player_ids.append(row[0])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn:
                cur.close()
                conn.close()
                print('Postgres connection closed.')
        return player_ids

    def get_team_data(self) -> dict:
        raw_team_dict = self._get_raw_data()['teams'][0]

        formatted_team_dict = {
            'id': raw_team_dict['id'],
            'venue_id': raw_team_dict['venue']['id'],
            'division_id': raw_team_dict['division']['id'],
            'conference_id': raw_team_dict['conference']['id'],
            'franchise_id': raw_team_dict['franchiseId'],
            'team_name': raw_team_dict['teamName'],
            'location': raw_team_dict['locationName'],
            'first_year_of_play': raw_team_dict['firstYearOfPlay'],
            'division_name': raw_team_dict['division']['name'],
            'conference_name': raw_team_dict['conference']['name'],
            'website': raw_team_dict['officialSiteUrl'],
            'active_flag': raw_team_dict['active']
        }

        return formatted_team_dict

    def get_team_stat_data(self) -> dict:
        raw_team_dict = self._get_raw_data()['stats'][0]['splits'][0]
        raw_team_stat_dict = raw_team_dict['stat']

        formatted_dict = {
            'team_id': raw_team_dict['team']['id'],
            'games_played': raw_team_stat_dict['gamesPlayed'],
            'wins': raw_team_stat_dict['wins'],
            'losses': raw_team_stat_dict['losses'],
            'overtime_losses': raw_team_stat_dict['ot'],
            'total_points': raw_team_stat_dict['pts'],
            'points_pct': float(raw_team_stat_dict['ptPctg']),
            'goals_per_game': raw_team_stat_dict['goalsPerGame'],
            'goals_against_per_game': raw_team_stat_dict['goalsAgainstPerGame'],
            'power_play_pct': float(raw_team_stat_dict['powerPlayPercentage']),
            'power_play_goals': raw_team_stat_dict['powerPlayGoals'],
            'power_play_goals_against': raw_team_stat_dict['powerPlayGoalsAgainst'],
            'power_play_opportunities': raw_team_stat_dict['powerPlayOpportunities'],
            'penalty_kill_pct': float(raw_team_stat_dict['penaltyKillPercentage']),
            'shots_per_game': raw_team_stat_dict['shotsPerGame'],
            'shots_allowed_per_game': raw_team_stat_dict['shotsAllowed'],
            'win_score_first_pct': raw_team_stat_dict['winScoreFirst'],
            'win_opponent_score_first_pct': raw_team_stat_dict['winOppScoreFirst'],
            'win_lead_first_period_pct': raw_team_stat_dict['winLeadFirstPer'],
            'win_lead_second_period_pct': raw_team_stat_dict['winLeadSecondPer'],
            'win_out_shoot_opponent_pct': raw_team_stat_dict['winOutshootOpp'],
            'win_out_shot_by_opponent_pct': raw_team_stat_dict['winOutshotByOpp'],
            'faceoffs_taken': raw_team_stat_dict['faceOffsTaken'],
            'faceoffs_won': raw_team_stat_dict['faceOffsWon'],
            'faceoffs_lost': raw_team_stat_dict['faceOffsLost'],
            'faceoffs_win_pct': float(raw_team_stat_dict['faceOffWinPercentage']),
            'shooting_pct': raw_team_stat_dict['shootingPctg'],
            'save_pct': raw_team_stat_dict['savePctg']
        }
        return formatted_dict

    def get_roster_data(self) -> list:
        """Returns list of dicts of roster data.
        This will be used as mapping data to the player table."""
        roster_list = []
        raw_roster_data = self._get_raw_data()['roster']

        for player in raw_roster_data:
            formatted_dict = {
                'player_id': int(player['person']['id']),
                'full_name': player['person']['fullName'],
                'jersey_number': int(player['jerseyNumber']),
                'position': player['position']['name']
            }
            roster_list.append(formatted_dict)

        return roster_list

    def get_player_regular_season_stats(self) -> list:
        """Returns a list of dicts, each dict being a player's on the roster stats
        for the season"""
        player_stats = []
        raw_player_data = self._get_raw_data()


