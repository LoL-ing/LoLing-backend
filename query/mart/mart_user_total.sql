-- 전체 승률 / kda
SELECT lol_name
     , COUNT(*) as total_count
     , AVG(IF(win, 1, 0)) as total_win_rate
     , IF(AVG(kills + assists - deaths) > 0, AVG(kills + assists - deaths), 0) as total_kda
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '꼽 죽'
 GROUP BY lol_name
 ORDER BY total_count desc
-- limit 2
;