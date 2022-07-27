from db_connection.rds import get_rds_db_connection, exec_query, exec_insert_query
from dotenv.main import load_dotenv
import os
import bcrypt
import jwt


load_dotenv()
secret_key = os.environ.get("SECRET_KEY")
algorithm = os.environ.get("ALGORITHM")


def get_user_info(user_id):
    rds_conn = get_rds_db_connection()
    user_data = {
        "user_id": user_id
    }
    select_query = """
    SELECT *
      FROM USER
     WHERE signin_id = %(user_id)s
    ;
    """
    user_response = exec_query(
        rds_conn, select_query, True, input_params=user_data)

    return user_response[0]


async def sign_in(email, password):
    is_exist = get_user_info(email)
    if is_exist:
        is_verified = bcrypt.checkpw(
            password.encode('utf-8'), bcrypt.hashpw(is_exist['password'].encode("utf-8"), bcrypt.gensalt()))
        if is_verified:
            token = jwt.encode({"email": email}, secret_key, algorithm)
            return token
            # return {"access_token": token, "token_type": "bearer"}
    else:
        return False


def register(user_id, password):

    return 0
