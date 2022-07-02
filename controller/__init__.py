from db_connection.mongo import get_db_connection
from db_connection.rds import get_rds_db_connection, exec_query
import json

def get_friends(flag = True, user_num = 0):
    rds_conn = get_rds_db_connection()
    select_query = """
    SELECT *
      FROM FRIENDS
    ;
    """

    return exec_query(rds_conn, select_query, True)


    """
    db = get_db_connection()
    response_data = list(db['Friends'].find())
    for data in response_data:
        data['_id'] = str(data['_id'])
        data = json.dumps(data, ensure_ascii=False).encode("utf8")
    if flag:
        return {"result" : response_data}
    else:
        return []
    """

def get_all_champions():
    collection_name = get_db_connection()
    return collection_name['Champions'].find()

def get_all_profiles():
    collection_name = get_db_connection()
    return collection_name['Profiles'].find()


