
SET SESSION group_concat_max_len = 100000;
-- 챔피언별 승률 / kda 을 LOL_ACCOUNT 에 추가
UPDATE USERS.LOL_ACCOUNT A
   SET A.champ_info = (SELECT CONCAT('[', 
                                GROUP_CONCAT(
                                  JSON_OBJECT(
                                    'QUEUE_TYPE', QUEUE_TYPE,
                                    'CHAMP_NAME', CHAMP_NAME,
                                    'CHAMP_COUNT', CHAMP_COUNT,
                                    'CHAMP_WIN_RATE', CHAMP_WIN_RATE,
                                    'CHAMP_KDA', CHAMP_KDA
                                  )
                        ORDER BY CHAMP_COUNT DESC
                                )
                                  , ']')
                         FROM (SELECT *
                                 FROM MATCHES.MART_USERS_CHAMP
                                WHERE LOL_NAME = '{{ params.lol_name }}'
                                  AND QUEUE_TYPE = '420'
                                ORDER BY CHAMP_COUNT desc) B
                      )
      , A.line_info = (SELECT CONCAT('[', 
                                GROUP_CONCAT(
                                  JSON_OBJECT(
                                    'QUEUE_TYPE', QUEUE_TYPE,
                                    'LINE_NAME', LINE_NAME,
                                    'LINE_COUNT', LINE_COUNT,
                                    'LINE_WIN_RATE', LINE_WIN_RATE,
                                    'LINE_KDA', LINE_KDA
                                  )
                        ORDER BY LINE_COUNT DESC
                                )
                                  , ']')
                         FROM (SELECT *
                                 FROM MATCHES.MART_USERS_LINE
                                WHERE LOL_NAME = '{{ params.lol_name }}'
                                  AND QUEUE_TYPE = '420'
                                ORDER BY LINE_COUNT desc) B
                      )
      , A.champ_info_sr = (SELECT CONCAT('[', 
                                GROUP_CONCAT(
                                  JSON_OBJECT(
                                    'QUEUE_TYPE', QUEUE_TYPE,
                                    'CHAMP_NAME', CHAMP_NAME,
                                    'CHAMP_COUNT', CHAMP_COUNT,
                                    'CHAMP_WIN_RATE', CHAMP_WIN_RATE,
                                    'CHAMP_KDA', CHAMP_KDA
                                  )
                        ORDER BY CHAMP_COUNT DESC
                                )
                                  , ']')
                         FROM (SELECT *
                                 FROM MATCHES.MART_USERS_CHAMP
                                WHERE LOL_NAME = '{{ params.lol_name }}'
                                  AND QUEUE_TYPE = '440'
                                ORDER BY CHAMP_COUNT desc) B
                      )
     , A.line_info_sr = (SELECT CONCAT('[', 
                                GROUP_CONCAT(
                                  JSON_OBJECT(
                                    'QUEUE_TYPE', QUEUE_TYPE,
                                    'LINE_NAME', LINE_NAME,
                                    'LINE_COUNT', LINE_COUNT,
                                    'LINE_WIN_RATE', LINE_WIN_RATE,
                                    'LINE_KDA', LINE_KDA
                                  )
                        ORDER BY LINE_COUNT DESC
                                )
                                  , ']')
                         FROM (SELECT *
                                 FROM MATCHES.MART_USERS_LINE
                                WHERE LOL_NAME = '{{ params.lol_name }}'
                                  AND QUEUE_TYPE = '440'
                                ORDER BY LINE_COUNT desc) B
                      )
 WHERE A.lol_name = '{{ params.lol_name }}'
;



-- # ################################################################################################################
-- SELECT CONCAT('[', GROUP_CONCAT(
--                     JSON_OBJECT(
--                     'QUEUE_TYPE', A.QUEUE_TYPE,
--                     'CHAMP_NAME', A.CHAMP_NAME,
--                     'CHAMP_COUNT', A.CHAMP_COUNT,
--                     'CHAMP_WIN_RATE', A.CHAMP_WIN_RATE,
--                     'CHAMP_KDA', A.CHAMP_KDA
--                                )
--                 )
--                                   , ']')
--   FROM (SELECT *
--           FROM MATCHES.MART_USERS_CHAMP
--          WHERE LOL_NAME = '고려대 김자헌'
--            AND QUEUE_TYPE = '420'
--          ORDER BY CHAMP_COUNT desc) A;