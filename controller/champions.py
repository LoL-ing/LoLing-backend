from db_connection.rds import get_rds_db_connection, exec_query

def get_all_champions():
    rds_conn = get_rds_db_connection()
    select_query = """
    SELECT *
      FROM CHAMPIONS
    ;
    """

    return exec_query(rds_conn, select_query, True)