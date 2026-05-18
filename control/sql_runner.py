import argparse
import psycopg2

db_config_west = {
    "dbname": "west_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5446"
}

db_config_east = {
    "dbname": "east_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5447"
}

db_config_warehouse = {
    "dbname": "warehouse_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5448"
}

db_config_mart = {
    "dbname": "mart_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5449"
}

configs = {
    "west": db_config_west,
    "east": db_config_east,
    "ware": db_config_warehouse,
    "mart": db_config_mart,
}

sqls = {
    "west": "lab1.sql",
    "east": "lab1.sql",
    "ware": "lab2.sql",
    "mart": "lab3.sql"
}

def run_sql(db_name, mode):
    config = configs[db_name]
    sql_filename = f"C:\\Users\\ajtal\\Desktop\\all\\база (ха-ха) данных\\3 year\\control\\sql\\{mode}\\{sqls[db_name]}"
    with open(sql_filename, "r") as sql_file:
        sql = sql_file.read()
        conn = psycopg2.connect(**config)
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db")
    parser.add_argument("mode", choices=["create", "drop"])
    args = parser.parse_args()
    run_sql(args.db, args.mode)
    print("SQL Done")
