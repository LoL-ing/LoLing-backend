from db_connection.rds import get_rds_db_connection, exec_query


def get_friends(flag=True, user_num=0):
    rds_conn = get_rds_db_connection()
    select_query = """
    SELECT *
      FROM USERS.USER_FRIEND_MAP
    ;
    """

    return exec_query(rds_conn, select_query, True)