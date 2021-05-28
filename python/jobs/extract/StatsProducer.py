import requests


AVS_TEAM_ENDPOINT = 'https://statsapi.web.nhl.com/api/v1/teams/21'


class StatsProducer:
    """Class that takes in a valid NHL API endpoint name as documented
    in the NHL API documentation github (see README.md) and returns that
    data as a formatted list of dictionaries.
    """
    def __init__(self):
        try:
            self.raw_data = requests.get(AVS_TEAM_ENDPOINT)
            self.raw_data.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        self.raw_team_data = self.raw_data.json()['teams'][0]

    def get_team_data(self) -> dict:
        raw_team_dict = self.raw_team_data

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

    def get_team_stats(self) -> dict:
        pass


if __name__ == '__main__':
    stats = StatsProducer()
    print(stats.get_team_data())
