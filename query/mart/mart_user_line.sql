-- 챔피언별 승률 / kda
SELECT lol_name
     , line_name
     , COUNT(line_name) AS line_count
     , AVG(IF(win, 1, 0)) as line_win_rate
     , AVG(kills + assists - deaths) as line_kda
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '꼽 죽'
 GROUP BY lol_name, line_name
 ORDER BY line_count desc
 limit 3
;