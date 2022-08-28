# LOL_ACCOUNT 정보를 모두 가져오기
SELECT_LOL_ACCOUNT = """
SELECT lol_name
     , tier
     , wins
     , losses
  FROM USERS.LOL_ACCOUNT
 WHERE LOL_NAME = %(lol_name)s;
"""


SELECT_USERS_LINE_STAT = """
SELECT *
  FROM MATCHES.MART_USER_BEST_LINE
 WHERE LOL_NAME = %(lol_name)s;
"""

SELECT_USERS_CHAMP_STAT = """
SELECT *
  FROM MATCHES.MART_USER_BEST_CHAMP
 WHERE LOL_NAME = %(lol_name)s;
"""
