-- Goal: Identify "High Velocity" spenders (people who spend a lot in a short window).

WITH UserSpending AS (
    SELECT 
        User_ID, 
        Amount, 
        Time,
        AVG(Amount) OVER(
            PARTITION BY User_ID 
            ORDER BY Time 
            ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
        ) as rolling_avg
    FROM transactions
)
SELECT *, 
       CASE 
           WHEN Amount > (rolling_avg * 3) THEN 'High Risk' 
           ELSE 'Normal' 
       END as Risk_Flag
FROM UserSpending;
