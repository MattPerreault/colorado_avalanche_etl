import requests


AVS_TEAM = {'endpoint': 'https://statsapi.web.nhl.com/api/v1/teams/21',
            'endpoint_name': 'team'}

AVS_TEAM_STATS = {'endpoint': 'https://statsapi.web.nhl.com/api/v1/teams/21/stats',
                  'endpoint_name': 'team stats'}

ENDPOINT_NAMES = ['team', 'team stats']
ENDPOINT_LIST = [AVS_TEAM, AVS_TEAM_STATS]


class StatsProducer:
    """Class that takes in a valid NHL API endpoint name as documented
    in the NHL API documentation github (see README.md) and returns that
    data as a formatted list of dictionaries.
    """
    def __init__(self, endpoint_name=AVS_TEAM['endpoint_name']):
        assert endpoint_name in ENDPOINT_NAMES, "Endpoint name not defined."
        self.endpoint = self._get_endpoint_url(endpoint_name)

        try:
            self.raw_data = requests.get(self.endpoint)
            self.raw_data.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def _get_endpoint_url(self, endpoint_name) -> str:
        """Returns the REST endpoint url for the given name."""
        ep_url = None
        for ep_dict in ENDPOINT_LIST:
            if ep_dict['endpoint_name'] == endpoint_name:
                ep_url = ep_dict['endpoint']
        return ep_url

    def _get_raw_data(self) -> dict:
        """Returns a JSON encoded dict list of raw data."""
        return self.raw_data.json()

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
        raw_team_dict = self._get_raw_data()
        return raw_team_dict
