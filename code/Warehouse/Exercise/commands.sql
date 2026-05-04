-- Show me the top three regions that have the most female riders as of the most recent date (2018-01-02).

CREATE OR REPLACE VIEW `dm_operational.top_3_region_by_female`
AS
SELECT
    region_id,name AS region_name,
    total_trips
FROM `dwh_bikesharing.fact_region_gender_daily_exercise`
WHERE DATE(trip_date) = DATE('2018-01-02') AND member_gender = 'Female'
ORDER BY total_trips desc
LIMIT 3;