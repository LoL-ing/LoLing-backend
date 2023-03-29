from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import mysql.connector
import mysql
from os import environ
from dotenv.main import load_dotenv

from app.common.config import settings

engine = create_engine(settings.DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
target_meta = Base.metadata


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_rds_db_connection() -> mysql.connector.connection.MySQLConnection:
    load_dotenv()
    conn = mysql.connector.connect(
        **{
            "host": settings.RDS_HOSTNAME,
            "user": settings.RDS_USERNAME,
            "password": settings.RDS_PASSWORD,
            "port": settings.RDS_PORT,
            "database": settings.RDS_DB_NAME,
        },
        autocommit=True,
    )

    return conn


def close_rds_db_connection(conn: mysql.connector.connection.MySQLConnection):
    conn.close()


# INSERT 문 (.SQL 파일 실행)
def exec_sql_file(sql_file, p_lol_name=""):
    try:
        conn = get_rds_db_connection()

        with open(sql_file, "r", encoding="UTF-8") as file:
            sql_staging = file.read()
            sql = sql_staging.replace("{{ params.lol_name }}", p_lol_name)
            # print(sql)
            cursor: mysql.connector.connection.MySQLCursor = conn.cursor()
            for result in cursor.execute(sql, multi=True):
                if result.with_rows:
                    result.fetchall()
                else:
                    print(
                        "Number of rows affected by statement {}: {}".format(
                            sql_file, result.rowcount
                        )
                    )

            conn.commit()

    except Exception as err:
        print(err)
        raise err

    finally:
        cursor.close()


# SELECT / DELETE 문


def exec_query(conn, query_str, select_flag=True, get_insert_id=False, input_params={}):
    try:
        conn = get_rds_db_connection()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor(
            dictionary=True)
        print(query_str)
        cursor.execute(query_str, input_params)

        if select_flag:
            result_list = cursor.fetchall()
            # print(cursor.statement)
            if get_insert_id:
                return cursor.lastrowid

            return result_list

    except Exception as err:
        raise err

    finally:
        close_rds_db_connection(conn)


# INSERT 문(여러 줄)


def exec_multiple_queries(conn, query_str, input_params=""):
    try:
        conn = get_rds_db_connection()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor()
        cursor.executemany(query_str, input_params)

    except Exception as err:
        raise err

    finally:
        cursor.close()


# INSERT (한줄)


def exec_insert_query(conn, query_str, input_params=""):
    try:
        conn = get_rds_db_connection()
        cursor: mysql.connector.connection.MySQLCursor = conn.cursor()
        cursor.execute(query_str, input_params)

    except Exception as err:
        raise err

    finally:
        cursor.close()
