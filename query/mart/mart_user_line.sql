
-- 라인별 승률 / kda
INSERT INTO MATCHES.MART_USER_BEST_LINE
SELECT lol_name as LOL_NAME
     , 'N/A' as QUEUE_TYPE
     , line_name as LINE_NAME
     , COUNT(line_name) AS LINE_COUNT
     , AVG(IF(win, 1, 0)) as LINE_WIN_RATE
     , IF(AVG(kills + assists - deaths) > 0, AVG(kills + assists - deaths), 0) as LINE_KDA
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '고려대 김자헌'
 GROUP BY lol_name, line_name
 ORDER BY LINE_COUNT desc
 -- limit 3
;