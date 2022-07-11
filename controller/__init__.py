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

def get_lol_account(flag = True, user_num = 0):
    rds_conn = get_rds_db_connection()
    select_query = """
    SELECT *
      FROM LOL_ACCOUNT
    ;
    """

    return exec_query(rds_conn, select_query, True)



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

def get_all_champions():
    collection_name = get_db_connection()
    return collection_name['Champions'].find()

def get_all_profiles():
    rds_conn = get_rds_db_connection()

    # JSON SEARCH 로 array 안의 것들을 join 할 수 있지만, 
    # 두 개 이상의 JSON ARRAY SEARCH 를 한다면, 3의 제곱의 row 가 나옴.
    # Img url 을 위해서 join 을 하는 것보다는, champion name 과 img url 코드를 통일시켜
    # 백엔드에서 만들어 보내주든지, 프론트에서 만들어 처리하는 것이 나을 듯
    # https://stackoverflow.com/questions/39818296/using-mysql-json-field-to-join-on-a-table
    # -김민규-
    # select_query = """
    #     SELECT A.*
    #         -- B.champion_name,
    #         -- B.image_uri 
    #         -- C.line_name
    #     FROM USER A
    #     -- LEFT OUTER JOIN CHAMPION B
    #         -- ON JSON_SEARCH(A.my_champ, 'one', B.champion_name)
    #     -- LEFT OUTER JOIN LINE C
    #         -- ON JSON_SEARCH(A.my_line, 'one', C.line_name)
    #     ;
    # """

    select_query = """
        select A.lol_name as nickname
            , B.name as lolingId
            , A.tier as tier
            , JSON_UNQUOTE(B.my_line) as line
            , JSON_UNQUOTE(A.champ_win_rate) as champ_win_rate
            , JSON_UNQUOTE(A.champ_kda) as champ_kda
            , JSON_UNQUOTE(A.line_win_rate) as line_winRate
            , JSON_UNQUOTE(A.line_kda) as line_kda
            , B.self_desc as description
          from LOL_ACCOUNT A
          left outer join USER B
            on A.lol_name = B.lol_name
        ;

    """
    profiles_response = exec_query(rds_conn, select_query, True)
    sample_data =   [{
        **data,
        "profileImg": "../assets/images/Nunu.png",
        "line": data.get("line")[0],
        "mannerTierImg": "../assets/images/Nunu.png",
        "championImg": "../assets/images/Nunu.png",
        "winRate": "100%",
        "winLose": "100%",
        "lineImg_1":"../assets/images/Nunu.png",
        "lineImg_2":"../assets/images/Nunu.png",
        "line_winRate_1":data.get("line_winRate")[0],
        "line_winRate_2":data.get("line_winRate")[1],
        "line_kda_1": data.get("line_kda")[0],
        "line_kda_2": data.get("line_kda")[1],
        "championImg_1":"../assets/images/Nunu.png",
        "championImg_2":"../assets/images/Nunu.png",
        "championImg_3":"../assets/images/Nunu.png",
        "champ_winRate_1": data.get("champ_win_rate")[0],
        "champ_winRate_2": data.get("champ_win_rate")[1],
        "champ_winRate_3": data.get("champ_win_rate")[2],
        "champ_kda_1": data.get("champ_kda")[0],
        "champ_kda_2": data.get("champ_kda")[1],
        "champ_kda_3": data.get("champ_kda")[2],
  } for data in profiles_response ] 

    return sample_data


