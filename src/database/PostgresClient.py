import psycopg2
from ..configuration.config import config


def initialize_db():
    """Open a connection to the postgres db"""
    conn = None
    try:
        db_creds = config.config()

        print('Connecting to the db...')
        conn = psycopg2.connect(**db_creds)
        cur = conn.cursor()

        print('postgres db version')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


initialize_db()
