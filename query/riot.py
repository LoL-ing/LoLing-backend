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


DELETE_USERS_MATCH_MAP = """
DELETE FROM MATCHES.USERS_MATCH_MAP
 WHERE lol_name = %(lol_name)s
;
"""

INSERT_USERS_MATCH_MAP = """
INSERT INTO MATCHES.USERS_MATCH_MAP (
       lol_name
     , match_id
     , match_type
     , ods_yn
) VALUES (
       %(lol_name)s
     , %(match_id)s
     , %(match_type)s
     , 'N'
)
;
"""

UPDATE_USERS_MATCH_ODS_YN = """
UPDATE MATCHES.USERS_MATCH_MAP
   SET ods_yn = %(ods_yn)s
 WHERE 1=1
"""

UPDATE_USERS_MATCH_ODS_YN_WHERE = """
   AND match_id in 
"""


SELECT_MATCH_ID_INFO_N = """
SELECT match_id
  FROM MATCHES.USERS_MATCH_MAP
 WHERE lol_name = %(lol_name)s
   AND ods_yn = 'N';
"""

INSERT_MATCH_INFO_ODS = """
INSERT INTO MATCHES.MATCHES_ODS (
       match_id
     , metadata
     , info
     , fact_yn
     , CREATED_DTTM
) VALUES (
       %(match_id)s
     , %(metadata)s
     , %(info)s
     , 'N'
     , NOW()
) 
   ON DUPLICATE KEY UPDATE match_id = VALUES(match_id)
                         , UPDATED_DTTM = NOW()
;
"""
