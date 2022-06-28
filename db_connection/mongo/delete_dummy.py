from db_connection.mongo import get_db_connection
db = get_db_connection()

for table_nm in ['Friends', 'Champions', 'Profiles']:
    coll = db[table_nm].find()
    for idx in range(len(list(coll))):
        db[table_nm].delete_one({})