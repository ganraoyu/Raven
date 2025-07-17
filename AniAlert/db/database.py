import sqlite3
import json
import os

DB_PATH = os.path.join("AniAlert", "db", "database.db")

# Create a global connection and cursor
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def create_tables_from_file(sql_file_path: str):
  with open(sql_file_path, 'r', encoding='utf-8') as f:
    sql_script = f.read()
  cursor.executescript(sql_script)
  conn.commit()

def print_table_contents():
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = cursor.fetchall()
  print("Tables:", tables)

  cursor.execute("SELECT * FROM anime_notify_list;")
  rows = cursor.fetchall()
  print("Rows in anime_notify_list:")
  for row in rows:
    print(json.dumps({
      "guild_id": row[1],
      "guild_name": row[2],
      "user_id": row[3],
      "user_name": row[4],
      "anime_name": row[5],
      "episode": row[6],
      "unix_air_time": row[7],
      "iso_air_time": row[8],
      "image": row[9],
      "episodes_list": json.loads(row[10]) if row[10] else []
    }, indent=2, ensure_ascii=False))

  cursor.execute("SELECT * FROM seasonal_schedule;")
  rows = cursor.fetchall()
  print("Rows in seasonal_schedule:")
  for row in rows:
    print(json.dumps({
      "id": row[0],
      "anime_name": row[1],
      "episode_number": row[2],
      "image": row[3],
      "airing_at": row[4]
    }, indent=2, ensure_ascii=False))

def close_connection():
  cursor.close()
  conn.close()

if __name__ == '__main__':
  create_tables_from_file(os.path.join("AniAlert", "db", "schema.sql"))
  print_table_contents()
  close_connection()
