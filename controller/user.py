from db_connection.rds import get_rds_db_connection, exec_query, exec_insert_query


def get_user_info(user_id):
    rds_conn = get_rds_db_connection()
    user_data = {
        "user_id": user_id
    }
    select_query = """
    SELECT *
      FROM USER
     WHERE phone_num = %(user_id)s
    ;
    """
    user_response = exec_query(
        rds_conn, select_query, True, input_params=user_data)

    return user_response


def sigin_in():
    return 0


def register(user_id, password):

    return 0
