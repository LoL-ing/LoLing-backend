-- 라인별 승률 / kda
SELECT lol_name
     , line_name
     , COUNT(line_name) AS 'line_count'
     , AVG(IF(win, 1, 0)) as line_win_rate
     , AVG(kills + assists - deaths) as line_kda
  FROM (
SELECT A.summoner_name AS lol_name
     , A.match_id AS match_id
     , A.queue_type AS match_type
     , 'Y' AS info_yn
     , JSON_EXTRACT(A.match_user_info, '$.lane') AS line_name
     , JSON_EXTRACT(A.match_user_info, '$.championName') AS champ_name
     , JSON_EXTRACT(A.match_user_info, '$.kills') AS kills
     , JSON_EXTRACT(A.match_user_info, '$.deaths') AS deaths
     , JSON_EXTRACT(A.match_user_info, '$.assists') AS assists
     , JSON_EXTRACT(A.match_user_info, '$.win') AS win
     , A.participants AS participants
     , NOW() AS CREATED_DTTM
     , NULL AS UPDATED_DTTM
     , A.game_version AS game_version
  FROM (SELECT a.match_id AS match_id
             , JSON_EXTRACT(a.metadata, '$.participants') AS participants
             , JSON_EXTRACT(a.info, '$.queueId') AS queue_type
             , JSON_EXTRACT(a.info, '$.gameVersion') as game_version
             , JSON_EXTRACT(a.info, CONCAT('$.participants[', b.ROW_NUM, ']')) AS match_user_info
             , JSON_EXTRACT(a.info, CONCAT('$.participants[', b.ROW_NUM, ']', '.summonerName')) AS summoner_name
          FROM MATCHES.MATCHES_ODS a
          LEFT OUTER JOIN NUMBER_ROWS b
                       ON b.ROW_NUM < 10
        ) A
 WHERE A.summoner_name = '고려대 김자헌'
    ) A
 GROUP BY lol_name, line_name

;

