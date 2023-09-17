import os
from configparser import ConfigParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def config(config="database.ini", section="postgres") -> dict:
    config = os.path.join(CURRENT_DIR, config)
    parser = ConfigParser()

    parser.read(config)

    db_creds = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_creds[param[0]] = param[1]

    else:
        raise Exception(f"Section {section} not found in the {config} file.")

    return db_creds
