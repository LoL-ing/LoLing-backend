-- 
DELETE
  FROM MATCHES.MART_USERS_CHAMP
 WHERE lol_name='{{ params.lol_name }}'
 ;


-- 챔피언별 승률 / kda
INSERT INTO MATCHES.MART_USERS_CHAMP
SELECT lol_name as LOL_NAME
     , '420' as QUEUE_TYPE
     , champ_name as CHAMPE_NAME
     , COUNT(champ_name) AS CHAMP_COUNT
     , AVG(IF(win, 1, 0)) AS CHAMP_WIN_RATE
     , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as CHAMP_KDA
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '{{ params.lol_name }}'
   AND A.queue_type = '420' -- 솔랭
 GROUP BY lol_name, champ_name
 ORDER BY CHAMP_COUNT desc
;

-- 챔피언별 승률 / kda
INSERT INTO MATCHES.MART_USERS_CHAMP
SELECT lol_name as LOL_NAME
     , '440' as QUEUE_TYPE
     , champ_name as CHAMPE_NAME
     , COUNT(champ_name) AS CHAMP_COUNT
     , AVG(IF(win, 1, 0)) AS CHAMP_WIN_RATE
     , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as CHAMP_KDA
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '{{ params.lol_name }}'
   AND A.queue_type = '440' -- 자랭
 GROUP BY lol_name, champ_name

 ORDER BY CHAMP_COUNT desc
;