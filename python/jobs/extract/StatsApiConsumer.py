import json
import requests


TEAMS_ENDPOINT = 'https://statsapi.web.nhl.com/api/v1/teams'


class StatsApiConsumer:
    def __init__(self):
        try:
            self.raw_data = requests.get(TEAMS_ENDPOINT)
            self.raw_data.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def get_teams(self):
        raw_dict = self.raw_data.json()
        for team_dict in raw_dict['teams']:
            print(f'{team_dict}\n')


if __name__ == '__main__':
    stats = StatsApiConsumer()
    stats.get_teams()
