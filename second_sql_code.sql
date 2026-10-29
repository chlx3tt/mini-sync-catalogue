CREATE OR REPLACE VIEW dbacademy.default.gold_catalogue AS
SELECT s.track_id, s.title, s.artist, s.play_count, s.genres,
       t.mood1, t.mood2, t.mood3,
       CAST(t.high_energy_yn AS INT) AS energy,
       t.vocal_type, t.language, UPPER(TRIM(t.explicit_yn)) AS explicit_yn,
       t.instrumentation_notes, t.theme1, t.theme2, t.theme3,
       t.best_for, t.sounds_like, t.pitch_note
FROM dbacademy.default.silver_catalogue s
JOIN dbacademy.default.my_tags_starter t USING (track_id);
