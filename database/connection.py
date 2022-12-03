import psycopg2

from utils.json_pocessing import open_json_file


def connect_to_db(create_db=False):
    creds = open_json_file("database/creds.json")
    root_db_name = "postgres"
    db_name = creds["db_name"] if create_db==False else root_db_name
    connect = psycopg2.connect(
        host=creds["host"],
        database=db_name,
        user=creds["user"],
        password=creds["password"]
    )
    return connect