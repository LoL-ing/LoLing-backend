import mysql.connector
import mysql
from os import environ
from dotenv.main import load_dotenv

def get_rds_db_connection() -> mysql.connector.connection.MySQLConnection:
    load_dotenv()
    conn = mysql.connector.connect(**{
        "host" : environ.get("RDS_HOSTNAME"),
        "user" : environ.get("RDS_USERNAME"),
        "password" : environ.get("RDS_PASSWORD"),
        "port" : environ.get("RDS_PORT"),
        "database" : environ.get("RDS_DB_NAME")
    }, autocommit=True)

    return conn

def close_rds_db_connection(conn : mysql.connector.connection.MySQLConnection):
    conn.close()

# SELECT 문
def exec_fetch_query(query_str, input_param="", get_insert_id=False):
    try:
        conn = get_rds_db_connection()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor(dictionary=True)
        cursor.execute(query_str, input_param)
        result_list = cursor.fetchall()

        # print(cursor.statement)
        if get_insert_id:
            return cursor.lastrowid

        return result_list

    finally:
        cursor.close()
        close_rds_db_connection(conn)
