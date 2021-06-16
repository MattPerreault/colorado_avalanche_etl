import argparse
import psycopg2

from configuration.config import config
from extract.StatsProducer import StatsProducer


class Runner:
    """Open a connection to the db on instantiation.
    A suite of methods to execute commands to the PosgreSQL db based
    on endpoint name passed into constructor.
    Leverages StatsProducer to get formatted endpoint data."""

    def __init__(self, endpoint_name):
        self.db_creds = config()
        self.conn = None
        self.cur = None
        self.endpoint_name = endpoint_name
        try:
            print('Connecting to the db...')
            self.conn = psycopg2.connect(**self.db_creds)
            self.cur = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_data(self):
        """Execute and commit INSERT statement to Postgres table
        Close connection when done"""

        formatted_data = self.get_endpoint_data()
        table = self.endpoint_name.replace(' ', '_')
        sql = Runner.build_insert_sql(table, formatted_data)

        query = self.cur.mogrify(sql, formatted_data)
        print(f'Executing insert on table {table}')
        self.cur.execute(query)

        print('Committing transaction...')
        self.conn.commit()

        self.cur.close()
        print('Database connection closed.')

    def get_endpoint_data(self) -> dict:
        """Returns formatted endpoint data."""
        formatted_dict = {}
        stats = StatsProducer(self.endpoint_name)
        if self.endpoint_name == 'team':
            formatted_dict = stats.get_team_data()
        elif self.endpoint_name == 'team stats':
            formatted_dict = stats.get_team_stat_data()
        elif self.endpoint_name == 'roster':
            formatted_dict = stats.get_roster_data()

        return formatted_dict

    @staticmethod
    def build_insert_sql(table, data) -> str:
        columns = ', '.join(data.keys())
        values = ','.join([f'%({k})s' for k in data.keys()])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        return sql


def get_cmd_line_args():
    parser = argparse.ArgumentParser(description='Insert extracted data to Postgres DB.')
    parser.add_argument('--endpointname',
                        dest='endpoint_name',
                        help='endpoint name see README.md for list.',
                        required=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = get_cmd_line_args()
    run = Runner(args.endpoint_name)
    run.insert_data()
