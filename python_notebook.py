# Databricks notebook source
dbutils.widgets.text("mood", "playful")
dbutils.widgets.text("theme", "celebration")
dbutils.widgets.dropdown("clean_only", "yes", ["yes", "no"])

cells = [r[0] for r in spark.sql(
    "SELECT DISTINCT best_for FROM dbacademy.default.gold_catalogue"
).collect() if r[0]]

phrases = sorted({p.strip() for c in cells for p in c.split(",") if p.strip()})

dbutils.widgets.dropdown("best_for", "", [""] + phrases)

mood  = dbutils.widgets.get("mood")
theme = dbutils.widgets.get("theme")
clean = dbutils.widgets.get("clean_only")
best_for = dbutils.widgets.get("best_for")

query = f"""
SELECT title, artist, play_count, language, best_for, pitch_note,
  (CASE WHEN mood1 = '{mood}' THEN 3
        WHEN mood2 = '{mood}' OR mood3 = '{mood}' THEN 1 ELSE 0 END
 + CASE WHEN theme1 = '{theme}' OR theme2 = '{theme}' OR theme3 = '{theme}'
        THEN 2 ELSE 0 END
 + CASE WHEN '{best_for}' <> ''
        AND lower(best_for) LIKE concat('%', lower('{best_for}'), '%')
        THEN 5 ELSE 0 END) AS score
FROM dbacademy.default.gold_catalogue
WHERE ('{clean}' = 'no' OR explicit_yn = 'N')
ORDER BY score DESC, play_count DESC
LIMIT 10
"""
display(spark.sql(query))
