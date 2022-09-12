
-- 챔피언별 승률 / kda 을 LOL_ACCOUNT 에 추가
UPDATE USERS.LOL_ACCOUNT A
   SET A.champ_info = (SELECT CONCAT('[', GROUP_CONCAT(
           JSON_OBJECT(
                   'QUEUE_TYPE', QUEUE_TYPE,
                   'CHAMP_NAME', CHAMP_NAME,
                   'CHAMP_COUNT', CHAMP_COUNT,
                   'CHAMP_WIN_RATE', CHAMP_WIN_RATE,
                   'CHAMP_KDA', CHAMP_KDA
               )
       )
                                  , ']')
                       FROM (SELECT lol_name                                                                as LOL_NAME
                                  , 'N/A'                                                                   as QUEUE_TYPE
                                  , champ_name                                                              as CHAMP_NAME
                                  , COUNT(champ_name)                                                       AS CHAMP_COUNT
                                  , AVG(IF(win, 1, 0))                                                      AS CHAMP_WIN_RATE
                                  , IF(AVG(kills + assists - deaths) > 0, AVG(kills + assists - deaths), 0) as CHAMP_KDA
                             FROM MATCHES.USERS_MATCH_HISTORY A
                             WHERE A.lol_name = '고려대 김자헌'
                             GROUP BY lol_name, champ_name
                             ORDER BY CHAMP_COUNT desc) B)
 WHERE A.lol_name = '고려대 김자헌'
;



-- 챔피언별 승률 / kda 을 LOL_ACCOUNT 에 추가
UPDATE USERS.LOL_ACCOUNT A
   SET A.line_info = (SELECT CONCAT('[', GROUP_CONCAT(
           JSON_OBJECT(
                   'QUEUE_TYPE', QUEUE_TYPE,
                   'LINE_NAME', LINE_NAME,
                   'LINE_COUNT', LINE_COUNT,
                   'LINE_WIN_RATE', LINE_WIN_RATE,
                   'LINE_KDA', LINE_KDA
               )
       )
                                  , ']')
                       FROM (SELECT lol_name                                                                as LOL_NAME
                                  , 'N/A'                                                                   as QUEUE_TYPE
                                  , line_name                                                              as LINE_NAME
                                  , COUNT(line_name)                                                       AS LINE_COUNT
                                  , AVG(IF(win, 1, 0))                                                      AS LINE_WIN_RATE
                                  , IF(AVG(kills + assists - deaths) > 0, AVG(kills + assists - deaths), 0) as LINE_KDA
                             FROM MATCHES.USERS_MATCH_HISTORY A
                             WHERE A.lol_name = '고려대 김자헌'
                             GROUP BY lol_name, line_name
                             ORDER BY LINE_COUNT desc) B)
 WHERE A.lol_name = '고려대 김자헌'
;