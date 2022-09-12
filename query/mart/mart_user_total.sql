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
  LEFT OUTER JOIN(
      SELECT lol_name
         , SUM(IF(win, 1, 0)) as win_count
         , SUM(IF(win, 0, 1)) as lose_count
         , COUNT(*) as total_count
         , AVG(IF(win, 1, 0)) as total_win_rate
         , IF(AVG((kills + assists) / IF(deaths = 0, 1, deaths)) > 0, AVG((kills + assists) / IF(deaths = 0, 1, deaths)), 0) as total_kda
        FROM MATCHES.USERS_MATCH_HISTORY A
       WHERE A.lol_name = '{{ params.lol_name }}'
         AND A.queue_type = '420'
       GROUP BY lol_name
       ORDER BY total_count desc
 ) C
    ON C.lol_name = B.lol_name
   SET B.total_win_rate = C.total_win_rate
     , B.total_kda = C.total_kda
     , B.wins = C.win_count
     , B.losses = C.lose_count
 WHERE C.lol_name = B.lol_name
;


-- 전체 승률, 전체 kda update
UPDATE USERS.LOL_ACCOUNT B
  LEFT OUTER JOIN(
      SELECT lol_name
         , SUM(IF(win, 1, 0)) as win_count
         , SUM(IF(win, 0, 1)) as lose_count
         , COUNT(*) as total_count
         , AVG(IF(win, 1, 0)) as total_win_rate
         , IF(AVG((kills + assists) / IF(deaths = 0, 1, deaths)) > 0, AVG((kills + assists) / IF(deaths = 0, 1, deaths)), 0) as total_kda
        FROM MATCHES.USERS_MATCH_HISTORY A
       WHERE A.lol_name = '{{ params.lol_name }}'
         AND A.queue_type = '440'
       GROUP BY lol_name
       ORDER BY total_count desc
 ) C
    ON C.lol_name = B.lol_name
   SET B.total_win_rate_sr = C.total_win_rate
     , B.total_kda_sr = C.total_kda
     , B.wins_sr = C.win_count
     , B.losses_sr = C.lose_count
 WHERE C.lol_name = B.lol_name
;
