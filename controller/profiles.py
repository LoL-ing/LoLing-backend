from db_connection.mongo import get_db_connection
from db_connection.rds import get_rds_db_connection, exec_query
import json


def get_lol_account(user_id: str, flag=True, user_num=0):
    rds_conn = get_rds_db_connection()
    where_arg = {"user_id": user_id}
    select_query = """
    SELECT C.*
         , JSON_UNQUOTE(C.champ_kda) as champ_kda
         , JSON_UNQUOTE(C.champ_win_rate) as champ_win_rate
         , JSON_UNQUOTE(C.line_kda) as line_kda
         , JSON_UNQUOTE(C.line_win_rate) as line_win_rate
      FROM USERS.USER A
      LEFT OUTER JOIN USERS.USER_LOL_ACCOUNT_MAP B
        ON A.SIGNIN_ID = B.SIGNIN_ID
      LEFT OUTER JOIN USERS.LOL_ACCOUNT C
        ON B.LOL_NAME = C.LOL_NAME
     WHERE A.SIGNIN_ID = %(user_id)s
    ;
    """

    lol_account = exec_query(rds_conn, select_query, True, input_params=where_arg)

    sample_data = [
        {
            "lol_name": data.get("lol_name"),
            "tier": data.get("tier"),
            "mostChampKDA": json.loads(data.get("champ_kda"))[1],
            "mostChampWinRate": json.loads(data.get("champ_win_rate"))[1],
            "mostLineKDA": json.loads(data.get("line_kda"))[1],
            "mostLineWinRate": json.loads(data.get("line_win_rate"))[1],
        }
        for data in lol_account
    ]

    return sample_data

    #     username: '하아아푸움',
    #     tier: 'Gold 3',
    #     mostChampImg: require('../assets/images/Nunu.png'),
    #     mostChampWinRate: '57%',
    #     mostChampKDA: '3.87',
    #     mostLineImg: require('../assets/images/lineJungle.png'),
    #     mostLineWinRate: '57%',
    #     mostLineKDA: '3.87',

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


def get_all_profiles(lol_name: str):
    rds_conn = get_rds_db_connection()
    where_arg = {"lol_name": lol_name}
    champ_query = """
    SELECT B.*
        , C.*
      FROM USERS.LOL_ACCOUNT A
      LEFT OUTER JOIN USERS.USER_CHAMPION_MAP B
        ON B.LOL_NAME = A.LOL_NAME
      LEFT OUTER JOIN CHAMPIONS C
        ON C.CHAMP_NAME = B.CHAMP_NAME
     WHERE A.LOL_NAME = %(lol_name)s
    ;
    """
    champ_response = exec_query(rds_conn, champ_query, True, input_params=where_arg)

    line_query = """
    SELECT B.*
         , C.*
      FROM USERS.LOL_ACCOUNT A
      LEFT OUTER JOIN USERS.USER_LINE_MAP B
        ON B.LOL_NAME = A.LOL_NAME
      LEFT OUTER JOIN LINE C
        ON C.LINE_NAME = B.LINE_NAME
     WHERE A.LOL_NAME = %(lol_name)s
     ;
    """
    line_response = exec_query(rds_conn, line_query, True, input_params=where_arg)

    # return {"champ": champ_response, "line": line_response}
    sample_data = {
        "lolingId": champ_response[0].get("lol_name"),
        "profileImg": "../assets/images/Nunu.png",
        "line": line_response[0].get("line_name"),
        "mannerTierImg": "../assets/images/diamond.png",
        "championImg": "../assets/images/Nunu.png",
        "winRate": "100%",
        "winLose": "100%",
        "lineImg_1": line_response[0].get("image_uri"),
        "lineImg_2": line_response[1].get("image_uri"),
        "line_winRate_1": line_response[0].get("line_win_rate"),
        "line_winRate_2": line_response[1].get("line_win_rate"),
        "line_kda_1": line_response[0].get("line_kda"),
        "line_kda_2": line_response[1].get("line_kda"),
        "championImg_1": champ_response[0].get("champ_img_url"),
        "championImg_2": champ_response[1].get("champ_img_url"),
        "championImg_3": champ_response[2].get("champ_img_url"),
        "champ_winRate_1": champ_response[0].get("champ_win_rate"),
        "champ_winRate_2": champ_response[1].get("champ_win_rate"),
        "champ_winRate_3": champ_response[2].get("champ_win_rate"),
        "champ_kda_1": champ_response[0].get("chmap_kda"),
        "champ_kda_2": champ_response[1].get("chmap_kda"),
        "champ_kda_3": champ_response[2].get("chmap_kda"),
    }

    return sample_data