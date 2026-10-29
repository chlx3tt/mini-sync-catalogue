CREATE OR REPLACE TABLE dbacademy.default.silver_catalogue AS
SELECT
  spotify_track_uri AS track_id,
  master_metadata_track_name AS title,
  master_metadata_album_artist_name AS artist,
  COUNT(*) AS play_count,
  SUM(listening_minutes) AS total_minutes,
  MIN(ts) AS first_played, MAX(ts) AS last_played,
  FIRST(genres) AS genres
FROM dbacademy.default.master_spotify_data_with_genres
WHERE spotify_track_uri IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY play_count DESC;
