
SET SESSION group_concat_max_len = 100000;
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
                                  , '420'                                                                     as QUEUE_TYPE
                                  , champ_name                                                                as CHAMP_NAME
                                  , COUNT(champ_name)                                                         AS CHAMP_COUNT
                                  , AVG(IF(win, 1, 0))                                                        AS CHAMP_WIN_RATE
                                  , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as CHAMP_KDA

                             FROM MATCHES.USERS_MATCH_HISTORY A
                             WHERE A.lol_name = '{{ params.lol_name }}'
                               AND A.queue_type = '420'
                             GROUP BY lol_name, champ_name
                             ORDER BY CHAMP_COUNT desc) B)
      , A.line_info = (SELECT CONCAT('[', GROUP_CONCAT(
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
                                  , '420'                                                                   as QUEUE_TYPE
                                  , line_name                                                               as LINE_NAME
                                  , COUNT(line_name)                                                        AS LINE_COUNT
                                  , AVG(IF(win, 1, 0))                                                      AS LINE_WIN_RATE
                                  , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as LINE_KDA

                             FROM MATCHES.USERS_MATCH_HISTORY A
                             WHERE A.lol_name = '{{ params.lol_name }}'
                               AND A.queue_type = '420'
                             GROUP BY lol_name, line_name
                             ORDER BY LINE_COUNT desc) B)
      , A.champ_info_sr = (SELECT CONCAT('[', GROUP_CONCAT(
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
                                  , '440'                                                                         as QUEUE_TYPE
                                  , champ_name                                                                    as CHAMP_NAME
                                  , COUNT(champ_name)                                                             AS CHAMP_COUNT
                                  , AVG(IF(win, 1, 0))                                                            AS CHAMP_WIN_RATE
                                  , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as CHAMP_KDA

                             FROM MATCHES.USERS_MATCH_HISTORY A
                             WHERE A.lol_name = '{{ params.lol_name }}'
                               AND A.queue_type = '440'
                             GROUP BY lol_name, champ_name
                             ORDER BY CHAMP_COUNT desc) B)
     , A.line_info_sr = (SELECT CONCAT('[', GROUP_CONCAT(
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
                                  , '440'                                                                        as QUEUE_TYPE
                                  , line_name                                                                    as LINE_NAME
                                  , COUNT(line_name)                                                             AS LINE_COUNT
                                  , AVG(IF(win, 1, 0))                                                           AS LINE_WIN_RATE
                                  , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as LINE_KDA

                             FROM MATCHES.USERS_MATCH_HISTORY A
                             WHERE A.lol_name = '{{ params.lol_name }}'
                               AND A.queue_type = '440'
                             GROUP BY lol_name, line_name
                             ORDER BY LINE_COUNT desc) B)
 WHERE A.lol_name = '{{ params.lol_name }}'
;