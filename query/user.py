# 유저 정보 조회
SELECT_USER = """
SELECT *
  FROM USERS.USER
 WHERE signin_id = %(user_id)s
;
"""

# 유저 정보 등록 -- 최초 회원가입 시
INSERT_USER_REGISER = """
INSERT INTO USERS.USER (
       signin_id
     , password
     , manner_tier
     , like_cnt
     , hate_cnt
     , created_at
     , updated_at
) VALUES (
     , %(email)s
     , %(password)s
     , '골드'
     , 0
     , 0
     , NOW()
     , NULL
)
"""

GET_USER_LOL_ACCOUNT = """
SELECT B.lol_name as lol_name
  FROM USERS.USER A
  LEFT OUTER JOIN USERS.USER_LOL_ACCOUNT_MAP B
    ON A.SIGNIN_ID = B.SIGNIN_ID
 WHERE A.SIGNIN_ID = %(email)s
;
"""
