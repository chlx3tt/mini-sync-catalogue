# Mini Sync Catalogue

**A sync-ready demo catalogue of my Spotify top played songs — tagged by a musician, backed by data.**

Built by Chloe (data analyst; steelpan, bass player) to demonstrate the full sync-catalogue workflow end to end: raw listening data → curated, DISCO-style metadata → a searchable catalogue that answers licensing briefs.

> **Honesty note:** This is a *demo* catalogue built to demonstrate workflow and metadata craft. I do not hold the rights to any of these tracks, and nothing here is offered for actual licensing.

## The pipeline (Databricks, medallion architecture)

| Layer | Table / view | What it is |
|---|---|---|
| **Bronze** | `master_spotify_data_with_genres` | My Spotify Extended Streaming History, Feb 2021 – Jun 2026: 57,086 plays, enriched with genre tags via the Last.fm API (the output of my Genre Preference Forecasting project) |
| **Silver** | `silver_catalogue` | One row per track: 5,132 unique tracks with play counts, total listening minutes, first/last played, genre tags. Personal fields (IP address etc.) never leave Bronze |
| **Tags** | `my_tags_starter` | 146 hand-picked tracks (top plays + Caribbean spine), each tagged by ear — see *The tagging system* below |
| **Gold** | `gold_catalogue` (view) | Silver ⨝ Tags on the exact Spotify track URI: 146 fully queryable catalogue rows, with cleaned types (energy as integer, explicit flag normalized). Re-tag and re-upload, and Gold updates itself |

## The tagging system

Every one of the 146 tracks was listened to and tagged by ear, using controlled vocabularies so the catalogue is *searchable*, not just labelled:

- **Moods** — 28 terms (`mood1` = the dominant, first-ten-seconds mood; briefs weight it highest)
- **Lyrical themes** — 25 terms (love, resilience, home, celebration…), plus attitude terms (swagger, confidence) where the track demanded them
- **Language** — tagged at dialect level, because Caribbean music deserves better than "English": Jamaican Patois (21 tracks), Trinidadian English Creole (17), Bajan Creole (3), Pidgin (2), Spanish (4), Korean (2)
- **Free-text where voice belongs**: instrumentation notes, `best_for` placement calls in my own words (72 distinct phrases — *carnival coverage bumper, cricket coverage, café scenes, villain scene, diaspora story scene*), `sounds_like` reference artists, and a one-line pitch note per track written to a supervisor

## The brief matcher (`03_brief_matcher`)

A Databricks notebook with widgets (mood, theme, best_for, clean-only toggle) that grades all 146 tracks against a brief:

- mood1 match **+3** · mood in slot 2/3 **+1** · theme match **+2** · best_for match **+2**
- `clean_only = yes` filters explicit tracks (brand briefs)
- Ties break by play count — sustained real listening as a momentum/familiarity signal

### Test briefs — actually run against the live catalogue

Each brief was first simulated from the raw tags, then run for real in Databricks. **The live run reproduced the simulated #1 pick in all six cases** — the tagging and the scoring are one consistent system.

| Brief | Widget settings | Top result |
|---|---|---|
| Streetwear campaign | mood swaggering · theme confidence | **Armanii — "Dunce Barbie"** (5 pts), then Armanii "Charge Up" and Aitch "Baby" |
| Villain entrance | mood aggressive · theme confidence | **King Von — "Took Her To The O"** (5 pts) |
| Empowerment anthem ad | mood confident · theme empowerment | **Kendrick Lamar — "Money Trees"** ("Not Like Us" also placed #4) |
| Rom-com meet-cute | mood playful · theme love · best_for meet-cute scenes | **New Edition — "Mr. Telephone Man"** (8 pts — the highest score of the test set) |
| Late-night drive | mood smooth · theme nightlife | **Lyrikal — "Loner"** |
| Caribbean tourism board ad | mood joyful · theme celebration · best_for Caribbean tourism ad | **Bad Bunny — "Baile Inolvidable"** (8 pts), then Tano "Jamtown" |

*<img width="1505" height="594" alt="streetwear" src="https://github.com/user-attachments/assets/1b34efbe-29ab-44fa-821a-457d8d0dc9d1" />
<img width="1504" height="614" alt="late-night-drive" src="https://github.com/user-attachments/assets/37c5d42d-d89a-4d1a-998b-e9c826f94ec4" />
<img width="1520" height="588" alt="meet-cute" src="https://github.com/user-attachments/assets/5c4366b3-11b1-414b-8569-b5f032618cf3" />
<img width="1498" height="615" alt="villain-entrance" src="https://github.com/user-attachments/assets/b583a92e-c2f8-4f6d-b8e5-88618a42faf8" />
<img width="1488" height="578" alt="caribbean-tourism" src="https://github.com/user-attachments/assets/d0ea6933-8382-4501-a468-94379d4aad51" />
<img width="1497" height="613" alt="empowerment" src="https://github.com/user-attachments/assets/f3bd1d92-44d1-4199-8176-f3f5fdffcbbb" />
*

### What the test runs caught (audit notes)

- **The cricket gap:** a cricket-coverage brief returns gospel tracks on the "triumphant" mood alone — no track in the catalogue carries a cricket `best_for`, although the lane was in the planning vocabulary. Fix queued: tag 2–3 soca anthems for cricket coverage, or retire the lane deliberately.
- **Score 0 means no match:** an ultra-specific brief (Trinidad tourism, clean-only) has exactly two scoring matches; below them, a `LIMIT 10` list pads with 0-score tracks ranked by play count. A real shortlist stops at the last scoring track.

## Stack

Databricks (Unity Catalog, Delta, Spark SQL) · Python / PySpark (matcher widgets & scoring) · Source data: Spotify Extended Streaming History + Last.fm API · Tagging workbook: Excel with data-validation dropdowns enforcing the vocabularies

## What I'd build next

- A `sounds_like` similarity layer (brief: "something like X, but Caribbean")

## Privacy

No raw listening history is published in this repo. The catalogue's play counts are aggregates over my own data; IP addresses and device fields exist only in the private Bronze table and are excluded from every downstream layer.
