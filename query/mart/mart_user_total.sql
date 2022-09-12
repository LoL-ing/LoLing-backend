-- SELECT lol_name
--      , COUNT(*) as total_count
--      , AVG(IF(win, 1, 0)) as total_win_rate
--      , IF(deaths = 0, AVG((kills + assists) / deaths), AVG((kills + assists)* 1.2)) as total_kda
--   FROM MATCHES.USERS_MATCH_HISTORY A
--  WHERE A.lol_name = '{{ params.lol_name }}'
--  GROUP BY lol_name
--  ORDER BY total_count desc
-- ;

-- 전체 승률, 전체 kda update
UPDATE USERS.LOL_ACCOUNT B
  LEFT OUTER JOIN
      (SELECT lol_name
     , COUNT(*) as total_count
     , AVG(IF(win, 1, 0)) as total_win_rate
     , IF(deaths = 0, AVG((kills + assists) / deaths), AVG((kills + assists)* 1.2)) as total_kda
  FROM MATCHES.USERS_MATCH_HISTORY A
 WHERE A.lol_name = '{{ params.lol_name }}'
 GROUP BY lol_name
 ORDER BY total_count desc) C
    ON C.lol_name=B.lol_name
   SET B.total_win_rate = C.total_win_rate
     , B.total_kda = C.total_kda
 WHERE C.lol_name=B.lol_name
;