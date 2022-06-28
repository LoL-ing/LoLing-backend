from db_connection.mongo import get_db_connection
import json

def get_friends(flag = True, user_num = 0):
    db = get_db_connection()
    response_data = list(db['Friends'].find())
    for data in response_data:
        data['_id'] = str(data['_id'])
        data = json.dumps(data, ensure_ascii=False).encode("utf8")
    if flag:
        return {"result" : response_data}
    else:
        return []

def get_all_champions():
    collection_name = get_db_connection()
    return collection_name['Champions'].find()

def get_all_profiles():
    collection_name = get_db_connection()
    return collection_name['Profiles'].find()


