DELETE_LOL_ACCOUNT = """
DELETE FROM USERS.LOL_ACCOUNT
 WHERE lol_name = %(lol_name)s
;
"""
INSERT_LOL_ACCOUNT = """
INSERT INTO USERS.LOL_ACCOUNT (
       lol_name
     , id
     , puuid
     , wins
     , losses
     , tier
) VALUES (
       %(lol_name)s 
     , %(user_id)s
     , %(puuid)s
     , %(wins)s
     , %(losses)s
     , %(tier)s
)
;
"""

DELETE_USER_LOL_ACCOUNT_MAP = """
DELETE FROM USERS.USER_LOL_ACCOUNT_MAP
 WHERE lol_name = %(lol_name)s
   AND signin_id = %(signin_id)s
;
"""

INSERT_USER_LOL_ACCOUNT_MAP = """
INSERT INTO USERS.USER_LOL_ACCOUNT_MAP (
       signin_id
     , lol_name
) VALUES (
       %(signin_id)s
     , %(lol_name)s
)
;
"""


DELETE_USERS_MATCH_HISTORY = """
DELETE FROM MATCHES.USERS_MATCH_HISTORY
 WHERE puuid = %(puuid)s
;
"""

INSERT_USERS_MATCH_HISTORY = """
INSERT INTO MATCHES.USERS_MATCH_HISTORY (
       puuid
     , match_id
     , match_type
     , info_yn
) VALUES (
       %(puuid)s
     , %(match_id)s
     , %(match_type)s
     , 'N'
)
;
"""

SELECT_MATCH_ID_INFO_N = """
SELECT puuid, match_id
  FROM MATCHES.USERS_MATCH_HISTORY
 WHERE info_yn = 'N';
"""

INSERT_MATCH_INFO_ODS = """
INSERT INTO MATCHES.MATCHES_ODS (
       metadata
     , info
) VALUES (
       %(metadata)s
     , %(info)s
) 
;
"""
