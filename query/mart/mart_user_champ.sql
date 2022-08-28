
-- 챔피언별 승률 / kda
INSERT INTO MATCHES.MART_USER_BEST_CHAMP
SELECT lol_name as LOL_NAME
     , 'N/A' as QUEUE_TYPE
     , champ_name as CHAMPE_NAME
     , COUNT(champ_name) AS CHAMP_COUNT
     , AVG(IF(win, 1, 0)) AS CHAMP_WIN_RATE
     , IF(AVG(kills + assists - deaths) > 0, AVG(kills + assists - deaths), 0) as CHAMP_KDA
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '고려대 김자헌'
 GROUP BY lol_name, champ_name
 ORDER BY CHAMP_COUNT desc
-- limit 2
;