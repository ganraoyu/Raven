CREATE TABLE IF NOT EXISTS anime_notify_list (
  id             SERIAL PRIMARY KEY,
  guild_id       BIGINT NOT NULL,
  guild_name     TEXT NOT NULL,
  user_id        BIGINT NOT NULL,
  user_name      TEXT NOT NULL, 
  anime_name     TEXT NOT NULL,
  episode        INTEGER,
  unix_air_time  BIGINT,
  iso_air_time   TEXT,
  image          TEXT,
  episodes_list  TEXT
);

CREATE TABLE IF NOT EXISTS seasonal_schedule (
  id             SERIAL PRIMARY KEY,
  anime_name     TEXT NOT NULL,
  episode_number INTEGER,
  airing_at_unix BIGINT,
  season         TEXT NOT NULL,
  year           INTEGER NOT NULL,
  image          TEXT
);
