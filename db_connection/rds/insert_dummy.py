from db_connection.rds import get_rds_db_connection, exec_multiple_queries, exec_query
def delete_friends():
    conn = get_rds_db_connection()
    delete_sql = """
    DELETE FROM FRIENDS
    """
    exec_query(conn, delete_sql, False)


def insert_friends():
    conn = get_rds_db_connection()
    friends_dummy = [
    {
        "user_id": "nomad",
        "friend_id": "bonobono",
    },

    {
        "user_id": "bonobono",
        "friend_id": "nomad",
    },
    ]
    insert_sql = """
    INSERT INTO FRIENDS (
        user_id,
        friend_id
    ) VALUES (
        %(user_id)s, %(friend_id)s
    )
    """
    exec_multiple_queries(conn, insert_sql, friends_dummy)