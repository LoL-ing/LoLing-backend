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
SELECT lol_name
  FROM USERS.LOL_ACCOUNT
 WHERE signin_id = %(email)s
;
"""

GET_FRIENDS_LOL_NAME = """
SELECT friend_lol_name 
  FROM USERS.LOL_FRIEND_MAP
 WHERE lol_name = %(lol_name)s
 ;
"""

# GET_FRIEND_PROFILES + lol_name +
# ';'
# 1. 아까 한 것처럼 dict
# 2. %s 를 써서 array
# 3. string concat

GET_FRIEND_PROFILES = """
SELECT *
  FROM USERS.LOL_ACCOUNT
 WHERE 1=1
"""

GET_FRIEND_PROFILES_WHERE = """
   AND lol_name in 
"""
