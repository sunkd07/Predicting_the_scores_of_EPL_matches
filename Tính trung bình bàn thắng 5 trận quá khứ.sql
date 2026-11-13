SELECT 
    game_id, home_team, home_goals,
    AVG(home_goals) OVER (
        PARTITION BY home_team 
        ORDER BY date 
        ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING
    ) AS rolling_avg_goals
FROM matches;