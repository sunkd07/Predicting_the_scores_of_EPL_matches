SELECT 
    game_id, home_team, away_team,
    (home_goals - away_goals) AS goal_diff,
    CASE 
        WHEN home_goals > away_goals THEN 'H'
        WHEN home_goals < away_goals THEN 'A'
        ELSE 'D'
    END AS match_result
FROM matches;
