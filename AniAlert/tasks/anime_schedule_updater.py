from AniAlert.services.anime_service import get_seasonal_schedule
from AniAlert.db.database import cursor, conn
from AniAlert.utils.seasonal_helper import get_season
from AniAlert.utils.time_helper import get_today_time

def table_exists(table_name: str) -> bool:
  cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name=?;
  """, (table_name,))

  return cursor.fetchone() is not None

def check_if_episode_exists(anime_name: str, episode_number: int) -> bool:
  select_query = '''
    SELECT 1 FROM seasonal_schedule 
    WHERE anime_name = ? AND episode_number = ?
    LIMIT 1
  '''

  cursor.execute(select_query, (anime_name, episode_number))
  result = cursor.fetchone()

  return result is not None

def update_anime_schedule():
  try:
    animes = get_seasonal_schedule()
    insert_query = '''
      INSERT INTO seasonal_schedule (
        anime_name, episode_number, airing_at_unix,
        season, year, image
      ) VALUES (?, ?, ?, ?, ?, ?)
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
        if not check_if_episode_exists(anime_name, episode_number):
          cursor.execute(insert_query, (
            anime_name, episode_number, airing_at_unix,
            season, year, image
          ))

    conn.commit()

  except Exception as e:
    print(f"[ERROR] Failed to update seasonal schedule: {e}")
    conn.rollback()

def delete_aired_episodes():  
  try:
    today, today_unix_midnight, current_unix_time = get_today_time()
    cursor.execute('SELECT anime_name, episode_number, airing_at_unix FROM seasonal_schedule')
    rows = cursor.fetchall()
    
    for row in rows:
      anime_name, episode_number, airing_at_unix = row

      if today_unix_midnight > airing_at_unix:
        print(f'Deleted: {anime_name} episode {episode_number}')

        delete_query = """
          DELETE FROM seasonal_schedule WHERE anime_name = ? AND episode_number = ?
        """
        cursor.execute(delete_query, (anime_name, episode_number))

    conn.commit()

  except Exception as e:
    print(f"[ERROR] Failed to delate aired episode: {e}")
    conn.rollback()

def get_schedule(table_name: str):
  if not table_exists(table_name):  
    print(table_exists(table_name))
    return 

update_anime_schedule()
delete_aired_episodes()