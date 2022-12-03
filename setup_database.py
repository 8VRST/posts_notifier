from utils.json_pocessing import open_json_file
from database.methods import create_database, create_table


db_data = open_json_file("database/creds.json")


create_database(db_data["db_name"])


create_table(name="links", columns=["id SERIAL PRIMARY KEY", "link text unique", "timestamp timestamp with time zone"])
create_table(name="users", columns=["id SERIAL PRIMARY KEY", "telegram_id bigint unique", "status bool",
                                    "lang text", "greet_status bool", "last_action timestamp with time zone"])
