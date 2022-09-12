INSERT INTO MATCHES.USERS_MATCH_HISTORY
SELECT A.summoner_name AS lol_name
     , A.match_id AS match_id
     , A.queue_type AS queue_type
     , JSON_UNQUOTE(JSON_EXTRACT(A.match_user_info, '$.lane')) AS line_name
     , JSON_UNQUOTE(JSON_EXTRACT(A.match_user_info, '$.championName')) AS champ_name
     , JSON_UNQUOTE(JSON_EXTRACT(A.match_user_info, '$.kills')) AS kills
     , JSON_UNQUOTE(JSON_EXTRACT(A.match_user_info, '$.deaths')) AS deaths
     , JSON_UNQUOTE(JSON_EXTRACT(A.match_user_info, '$.assists')) AS assists
     , JSON_UNQUOTE(JSON_EXTRACT(A.match_user_info, '$.win')) AS win
     , A.participants AS participants
     , NOW() AS CREATED_DTTM
     , NULL AS UPDATED_DTTM
     , A.game_version AS game_version
  FROM (SELECT a.match_id AS match_id
             , JSON_UNQUOTE(JSON_EXTRACT(a.metadata, '$.participants')) AS participants
             , JSON_UNQUOTE(JSON_EXTRACT(a.info, '$.queueId')) AS queue_type
             , JSON_UNQUOTE(JSON_EXTRACT(a.info, '$.gameVersion')) as game_version
             , JSON_UNQUOTE(JSON_EXTRACT(a.info, CONCAT('$.participants[', b.ROW_NUM, ']'))) AS match_user_info
             , JSON_UNQUOTE(JSON_EXTRACT(a.info, CONCAT('$.participants[', b.ROW_NUM, ']', '.summonerName'))) AS summoner_name
          FROM (SELECT *
                  FROM MATCHES.MATCHES_ODS
                 WHERE fact_yn = 'N'
          ) a
          LEFT OUTER JOIN LoLing.NUMBER_ROWS b
                       ON b.ROW_NUM < 10
        ) A
   ON DUPLICATE KEY UPDATE UPDATED_DTTM = NOW()
;

UPDATE MATCHES.MATCHES_ODS 
   SET fact_yn = 'Y'
 WHERE fact_yn = 'N'
;