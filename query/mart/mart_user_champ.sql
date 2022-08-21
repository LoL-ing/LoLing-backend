-- 챔피언별 승률 / kda
SELECT lol_name
     , champ_name
     , COUNT(champ_name) AS champ_count
     , AVG(IF(win, 1, 0)) as champ_win_rate
     , AVG(kills + assists - deaths) as champ_kda
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '꼽 죽'
 GROUP BY lol_name, champ_name
 ORDER BY champ_count desc
 limit 3
;