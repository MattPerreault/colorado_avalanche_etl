from configparser import ConfigParser


def config(config='database.ini', section='postgres') -> dict:
    parser = ConfigParser()

    parser.read(config)

    db_creds = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_creds[param[0]] = param[1]

    else:
        raise Exception(f'Section {section} not found in the {config} file.')

    return db_creds
