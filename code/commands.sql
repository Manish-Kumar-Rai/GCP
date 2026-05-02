-- 1. How many bike trips take place daily?
CREATE OR REPLACE TABLE `gcp-learning-494920.dm_operational.bike_trips_daily`
AS
SELECT
  trip_date, SUM(total_trips) AS total_trips_daily 
FROM `gcp-learning-494920.dwh_bikesharing.fact_daily_trips`
GROUP BY trip_date;



-- 2.What is the daily average trip duration?
CREATE OR REPLACE TABLE `gcp-learning-494920.dm_operational.daily_avg_trips_duration`
AS
SELECT
  trip_date, ROUND(AVG(avg_duration_sec)) AS daily_avg_duration_sec 
FROM `gcp-learning-494920.dwh_bikesharing.fact_daily_trips`
GROUP BY trip_date;


-- 3.What are the top five station names of starting stations with the longest trip duration?
CREATE VIEW `gcp-learning-494920.dm_operational.top_5_station_by_longest_duration`
AS
SELECT trip_date, station_name, sum_duration_sec
FROM `gcp-learning-494920.dwh_bikesharing.fact_daily_trips`
JOIN `gcp-learning-494920.dwh_bikesharing.dim_stations`
ON start_station_id = station_id
WHERE trip_date = '2018-01-02'
ORDER BY sum_duration_sec desc
LIMIT 5;



-- 4.What are the top three region names that have the shortest total trip durations?
CREATE VIEW dm_operational.top_3_region_by_shortest_duration
AS
SELECT trip_date, region_name, SUM(sum_duration_sec) as
total_sum_duration_sec
FROM dwh_bikesharing.fact_daily_trips
JOIN dwh_bikesharing.dim_stations
ON start_station_id = station_id
WHERE trip_date = '2018-01-02'
GROUP BY trip_date, region_name
ORDER BY total_sum_duration_sec asc
LIMIT 3;