from AniAlert.services.anime_service import get_seasonal_schedule
from AniAlert.db.database import cursor, conn

def table_exists(table_name: str) -> bool:
  cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name=?;
  """, (table_name,))

  return cursor.fetchone() is not None

def update_anime_schedule():
  animes = get_seasonal_schedule()

def get_seasonal_schedule(table_name: str):
  if not table_exists(table_name):  
    print(table_exists(table_name))
    return 
  
get_seasonal_schedule('airing_schedule')

  
