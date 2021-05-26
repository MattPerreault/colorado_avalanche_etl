import requests


AVS_TEAM_ENDPOINT = 'https://statsapi.web.nhl.com/api/v1/teams/21'


class StatsApiConsumer:
    def __init__(self):
        try:
            self.raw_data = requests.get(AVS_TEAM_ENDPOINT)
            self.raw_data.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def get_team_data(self) -> dict:
        print(self.raw_data.json())


if __name__ == '__main__':
    stats = StatsApiConsumer()
    stats.get_team_data()
