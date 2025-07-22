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
  
  inserted_count = 0
  
  for anime in animes:
    start_date = anime.get('start_date', {})
    if not start_date:
      continue

    anime_name = anime.get('title')
    image = anime.get('image')
    month = start_date.get('month')
    year = start_date.get('year')
    
    if not anime_name or not month or not year:
      continue
      
    season = get_season(month)

    episodes = anime.get('airing_schedule', [])
    for episode in episodes:
      episode_number = episode.get('episode')
      airing_at_unix = episode.get('airing_at_unix')
      
      if episode_number is None or airing_at_unix is None:
        continue
        
      if not check_if_episode_exists(anime_name, episode_number, cursor):
        cursor.execute(insert_query, (
          anime_name, episode_number, airing_at_unix,
          season, year, image
        ))
        inserted_count += 1
  
  print(f"[INFO] Inserted {inserted_count} new episodes into schedule")

def delete_aired_episodes(cursor):
  today, today_unix_midnight, current_unix_time, yesterday_unix_midnight = get_today_time()
  cursor.execute('SELECT anime_name, episode_number, airing_at_unix FROM seasonal_schedule')
  rows = cursor.fetchall()
  
  deleted_count = 0
  
  for row in rows:
    anime_name, episode_number, airing_at_unix = row
    
    # Delete episodes that aired more than 24 hours (86400 seconds) ago
    if current_unix_time > (airing_at_unix + 86400):
      print(f'[INFO] Deleting episode that aired 24+ hours ago: {anime_name} episode {episode_number}')
      delete_query = f"""
        DELETE FROM seasonal_schedule WHERE anime_name = {placeholder} AND episode_number = {placeholder}
      """
      cursor.execute(delete_query, (anime_name, episode_number))
      deleted_count += 1
  
  print(f"[INFO] Deleted {deleted_count} episodes that aired 24+ hours ago")

def refresh_schedule():
  conn = get_db_connection()
  cursor = conn.cursor()

  try:
    print(f"[INFO] Starting schedule refresh at {time.ctime()}")
    
    # Delete old episodes first
    delete_aired_episodes(cursor)
    
    # Then update with new episodes  
    update_anime_schedule(cursor)
    
    # Check final count
    cursor.execute("SELECT COUNT(*) FROM seasonal_schedule")
    count = cursor.fetchone()[0]
    print(f"[INFO] Schedule refresh complete. Total episodes: {count}")
    
    conn.commit()

  except Exception as e:
    print(f"[ERROR] Failed to refresh schedule: {e}")
    import traceback
    traceback.print_exc()
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