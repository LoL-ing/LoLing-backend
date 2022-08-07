import mysql.connector
import mysql
from os import environ
import logging
from exception import LOLINGDBRequestFailException
from dotenv.main import load_dotenv


def get_rds_db_connection() -> mysql.connector.connection.MySQLConnection:
    load_dotenv()
    conn = mysql.connector.connect(**{
        "host": environ.get("RDS_HOSTNAME"),
        "user": environ.get("RDS_USERNAME"),
        "password": environ.get("RDS_PASSWORD"),
        "port": environ.get("RDS_PORT"),
        "database": environ.get("RDS_DB_NAME")
    }, autocommit=True)

    return conn


def close_rds_db_connection(conn: mysql.connector.connection.MySQLConnection):
    conn.close()

# SELECT / DELETE 문

def exec_query(conn, query_str, select_flag=True, get_insert_id=False, input_params=""):
    try:
        conn = get_rds_db_connection()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor(
            dictionary=True)
        cursor.execute(query_str, input_params)

        if select_flag:
            result_list = cursor.fetchall()
            # print(cursor.statement)
            if get_insert_id:
                return cursor.lastrowid

            return result_list
    
    except Exception as err:
        logging.getLogger("logger").error("쿼리 실행 중 오류가 발생했습니다 :  " + repr(err))
        raise LOLINGDBRequestFailException(err)

    finally:
        close_rds_db_connection(conn)


# INSERT 문(여러 줄)

def exec_multiple_queries(conn, query_str, input_params=""):
    try:
        conn = get_rds_db_connection()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor()
        cursor.executemany(query_str, input_params)

    except Exception as err:
        logging.getLogger("logger").error("쿼리 실행 중 오류가 발생했습니다 :  " + repr(err))
        raise LOLINGDBRequestFailException(err)

    finally:
        cursor.close()

# INSERT (한줄)

def exec_insert_query(conn, query_str, input_params=""):
    try:
        conn = get_rds_db_connection()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor()
        cursor.execute(query_str, input_params)

    except Exception as err:
        logging.getLogger("logger").error("쿼리 실행 중 오류가 발생했습니다 :  " + repr(err))
        raise LOLINGDBRequestFailException(err)

    finally:
        cursor.close()
