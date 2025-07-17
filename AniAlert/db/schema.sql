CREATE TABLE IF NOT EXISTS anime_notify_list (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  guild_id       INTEGER NOT NULL,
  guild_name     TEXT NOT NULL,
  user_id        INTEGER NOT NULL,
  user_name      TEXT NOT NULL, 
  anime_name     TEXT NOT NULL,
  episode        INTEGER,
  unix_air_time  INTEGER,
  iso_air_time   TEXT,
  image          TEXT,
  episodes_list  TEXT
);

CREATE TABLE IF NOT EXISTS seasonal_schedule (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  anime_name     TEXT NOT NULL,
  episode_number INTEGER,
  airing_at_unix INTEGER,
  season         TEXT NOT NULL,
  year           INT NOT NULL,
  image          TEXT
);