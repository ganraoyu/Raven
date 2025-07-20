import time
import threading
import os

from AniAlert.services.anime_service import get_seasonal_schedule
from AniAlert.utils.seasonal_helper import get_season
from AniAlert.utils.time_helper import get_today_time
from AniAlert.db.database import get_db_connection, get_placeholder

placeholder = get_placeholder()

def check_if_episode_exists(anime_name: str, episode_number: int, cursor) -> bool:
  select_query = f'''
    SELECT 1 FROM seasonal_schedule 
    WHERE anime_name = {placeholder} AND episode_number = {placeholder}
    LIMIT 1
  '''
  cursor.execute(select_query, (anime_name, episode_number))
  return cursor.fetchone() is not None

def update_anime_schedule(cursor):
  animes = get_seasonal_schedule()
  insert_query = f'''
    INSERT INTO seasonal_schedule (
      anime_name, episode_number, airing_at_unix,
      season, year, image
    ) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
  '''
  for anime in animes:
    start_date = anime.get('start_date', {})
    if not start_date:
      continue

    anime_name = anime.get('title')
    image = anime.get('image')
    month = start_date.get('month')
    year = start_date.get('year')
    season = get_season(month)

    episodes = anime.get('airing_schedule', [])
    for episode in episodes:
      episode_number = episode.get('episode')
      airing_at_unix = episode.get('airing_at_unix')
      if not check_if_episode_exists(anime_name, episode_number, cursor):
        cursor.execute(insert_query, (
          anime_name, episode_number, airing_at_unix,
          season, year, image
        ))

def delete_aired_episodes(cursor):
  _, today_unix_midnight, _ = get_today_time()
  cursor.execute('SELECT anime_name, episode_number, airing_at_unix FROM seasonal_schedule')
  rows = cursor.fetchall()
  for row in rows:
    anime_name, episode_number, airing_at_unix = row
    if today_unix_midnight > airing_at_unix:
      print(f'Deleted: {anime_name} episode {episode_number}')
      delete_query = f"""
        DELETE FROM seasonal_schedule WHERE anime_name = {placeholder} AND episode_number = {placeholder}
      """
      cursor.execute(delete_query, (anime_name, episode_number))

def refresh_schedule():
  conn = get_db_connection()
  cursor = conn.cursor()

  try:
    update_anime_schedule(cursor)
    delete_aired_episodes(cursor)
    print(f"Seasonal Schedule Refreshed at {time.ctime()}")
    conn.commit()

  except Exception as e:
    print(f"[ERROR] Failed to refresh schedule: {e}")
    conn.rollback()

  finally:
    cursor.close()
    conn.close()

def run_schedule_loop(interval_seconds: int = 604800):
  def loop():
    while True:
      refresh_schedule()
      time.sleep(interval_seconds)

  threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
  conn = get_db_connection()
  conn.close()

  refresh_schedule()  
  print("Anime schedule updater started.")