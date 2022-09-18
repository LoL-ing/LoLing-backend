from db_connection.mongo import get_db_connection
from db_connection.rds import get_rds_db_connection, exec_query
from fastapi import APIRouter, Depends
from operator import itemgetter
import json
from starlette.responses import JSONResponse
from starlette.status import *

from query.profiles import (
    SELECT_LOL_ACCOUNT,
    SELECT_USERS_CHAMP_STAT,
    SELECT_USERS_LINE_STAT,
)


def get_lol_account(user_id: str, flag=True, user_num=0):
    rds_conn = get_rds_db_connection()
    where_arg = {"user_id": user_id}
    select_query = """
    SELECT C.*
         , JSON_UNQUOTE(C.CHAMP_INFO) AS CHAMP_INFO
         , JSON_UNQUOTE(C.LINE_INFO) AS LINE_INFO
      FROM USERS.USER A
      LEFT OUTER JOIN USERS.LOL_ACCOUNT C
        ON C.LOL_NAME = A.CURR_LOL_ACCOUNT
       AND C.SIGNIN_ID = A.SIGNIN_ID
     WHERE A.SIGNIN_ID = %(user_id)s
    ;
    """

    lol_account = exec_query(rds_conn, select_query, True, input_params=where_arg)

    if isinstance(lol_account, list) and len(lol_account) > 0:
        lol_account = lol_account[0]
    else:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content=dict(msg="id 에 해당하는 lol_account 를 찾지 못함"),
        )

    champ_info = (
        json.loads(lol_account.get("CHAMP_INFO"))
        if lol_account.get("CHAMP_INFO") != None
        else [{} for _ in range(3)]
    )
    line_info = (
        json.loads(lol_account.get("LINE_INFO"))
        if lol_account.get("LINE_INFO") != None
        else [{} for _ in range(3)]
    )

    sample_data = {
        "lol_name": lol_account.get("lol_name"),
        "tier": lol_account.get("tier"),
        "mostChampKDA": champ_info[0].get("CHAMP_KDA"),
        "mostChampWinRate": champ_info[0].get("CHAMP_WIN_RATE"),
        "mostLineKDA": line_info[0].get("LINE_KDA"),
        "mostLineWinRate": line_info[0].get("LINE_WIN_RATE"),
    }

    return sample_data


def get_profile(lol_name: str):
    # LOL_ACCOUNT, MART_BEST_USER_LINE, MART_BEST_USER_CHAMP 테이블 받아오기
    rds_conn = get_rds_db_connection()
    where_arg = {"lol_name": lol_name}

    lol_account = exec_query(rds_conn, SELECT_LOL_ACCOUNT, input_params=where_arg)

    lol_account = list(
        map(
            lambda data: {
                **data,
                "champ_info": json.loads(data.get("champ_info"))
                if data.get("champ_info") not in ["", None]
                else [{} for _ in range(3)],
                "line_info": json.loads(data.get("line_info"))
                if data.get("line_info") not in ["", None]
                else [{} for _ in range(3)],
                "champ_info_sr": json.loads(data.get("champ_info_sr"))
                if data.get("champ_info_sr") not in ["", None]
                else [{} for _ in range(3)],
                "line_info_sr": json.loads(data.get("line_info_sr"))
                if data.get("line_info_sr") not in ["", None]
                else [{} for _ in range(3)],
            },
            lol_account,
        )
    )
    # champ 와 line info를 별개로 가져오며 orderby 를 하게 되면 DB 3
    #번 찍러야 하는 문제 발생 
    # 
    # dict 형식으로 바꿔준건가? ㅇㅇ 그런거지
    #lol_account.champ_info.sort(key=itemgetter(4),reverse=True)

    return {**lol_account[0]}
