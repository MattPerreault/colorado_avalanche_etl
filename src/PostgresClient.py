import psycopg2

from configuration.config import config
from extract.StatsProducer import StatsProducer


def insert_team_data():
    """Open a connection to the postgres db
    execute INSERT statement to team table"""
    conn = None

    stats_producer = StatsProducer()

    team_dict = stats_producer.get_team_data()

    sql = build_insert_sql('team', team_dict)

    try:
        db_creds = config()

        print('Connecting to the db...')
        conn = psycopg2.connect(**db_creds)
        cur = conn.cursor()

        query = cur.mogrify(sql, team_dict)

        cur.execute(query)

        conn.commit()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def build_insert_sql(table, data) -> str:
    columns = ', '.join(data.keys())
    values = ','.join([f'%({k})s' for k in data.keys()])
    sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

    return sql


insert_team_data()
