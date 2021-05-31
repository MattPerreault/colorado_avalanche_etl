import psycopg2

from configuration.config import config
from extract.StatsProducer import StatsProducer


class Runner:
    """Open a connection to the db on instantiation.
    A suite of methods to execute commands to the PosgreSQL db.
    Leverages StatsProducer to which API endpoints to pull from."""

    def __init__(self):
        self.db_creds = config()
        self.conn = None
        self.cur = None

        try:
            print('Connecting to the db...')
            self.conn = psycopg2.connect(**self.db_creds)
            self.cur = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_team_data(self):
        """Execute and commit INSERT statement to team table
        Close connection when done"""

        stats_producer = StatsProducer('team')
        team_dict = stats_producer.get_team_data()

        sql = Runner.build_insert_sql('team', team_dict)

        query = self.cur.mogrify(sql, team_dict)
        print('Executing insert...')
        self.cur.execute(query)

        print('Committing transaction...')
        self.conn.commit()

        self.cur.close()
        print('Database connection closed.')

    @staticmethod
    def build_insert_sql(table, data) -> str:
        columns = ', '.join(data.keys())
        values = ','.join([f'%({k})s' for k in data.keys()])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        return sql


if __name__ == '__main__':
    run = Runner()
    
