-- 
DELETE
  FROM MATCHES.MART_USERS_LINE
 WHERE lol_name='{{ params.lol_name }}'
 ;


-- 라인별 승률 / kda
INSERT INTO MATCHES.MART_USERS_LINE
SELECT lol_name as LOL_NAME
     , '420' as QUEUE_TYPE
     , line_name as LINE_NAME
     , COUNT(line_name) AS LINE_COUNT
     , AVG(IF(win, 1, 0)) as LINE_WIN_RATE
     , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as LINE_KDA
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '{{ params.lol_name }}'
   AND A.queue_type = '420'
 GROUP BY lol_name, line_name
 ORDER BY LINE_COUNT desc
 -- limit 3
;

INSERT INTO MATCHES.MART_USERS_LINE
SELECT lol_name as LOL_NAME
     , '440' as QUEUE_TYPE
     , line_name as LINE_NAME
     , COUNT(line_name) AS LINE_COUNT
     , AVG(IF(win, 1, 0)) as LINE_WIN_RATE
     , (AVG(kills) + AVG(assists)) / IF(AVG(deaths) <> 0, AVG(deaths), 1) as LINE_KDA
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '{{ params.lol_name }}'
   AND A.QUEUE_TYPE = '440'
 GROUP BY lol_name, line_name
 ORDER BY LINE_COUNT desc
 -- limit 3
;