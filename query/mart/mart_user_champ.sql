-- 챔피언별 승률 / kda
SELECT lol_name
     , champ_name
     , COUNT(champ_name) AS champ_count
     , AVG(IF(win, 1, 0)) as champ_win_rate
     , IF(AVG(kills + assists - deaths) > 0, AVG(kills + assists - deaths), 0) as champ_kda
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '고려대 김자헌'
 GROUP BY lol_name, champ_name
 ORDER BY champ_count desc
-- limit 2
;