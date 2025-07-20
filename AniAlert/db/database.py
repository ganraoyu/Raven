import sqlite3
import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # 'sqlite' or 'postgres'

# SQLite local config
DB_PATH = os.path.join("AniAlert", "db", "database.db")

# PostgreSQL config
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 5432))

def get_placeholder():
  return "?" if DB_TYPE == "sqlite" else "%s"

def get_db_connection():
  if DB_TYPE == "sqlite":
    return sqlite3.connect(DB_PATH, check_same_thread=True)
  elif DB_TYPE == "postgres":
    return psycopg2.connect(
      host=DB_HOST,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      port=DB_PORT
    )
  else:
    raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")

conn = get_db_connection()
cursor = conn.cursor()

def create_tables_from_file(sql_file_path: str):
  with open(sql_file_path, 'r', encoding='utf-8') as f:
    sql_script = f.read()

  if DB_TYPE == "sqlite":
    cursor.executescript(sql_script)
  else:
    statements = sql_script.split(';')
    for stmt in statements:
      stmt = stmt.strip()
      if stmt:
        cursor.execute(stmt)
  conn.commit()

def print_table_contents():
  if DB_TYPE == "sqlite":
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  else:
    cursor.execute("""
      SELECT table_name 
      FROM information_schema.tables
      WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    """)
  tables = cursor.fetchall()
  print("Tables:", tables)

  # Query anime_notify_list
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

  # Query seasonal_schedule
  cursor.execute("SELECT * FROM seasonal_schedule;")
  rows = cursor.fetchall()
  print("Rows in seasonal_schedule:")
  for row in rows:
    print(json.dumps({
      "id": row[0],
      "anime_name": row[1],
      "episode_number": row[2],
      "airing_at_unix": row[3],
      "season": row[4],
      "year": row[5],
      "image": row[6]
    }, indent=2, ensure_ascii=False))

def delete_all_data():
    if DB_TYPE == "sqlite":
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
      tables = cursor.fetchall()
      for (table_name,) in tables:
        if table_name.startswith('sqlite_'):  
          continue
        cursor.execute(f"DELETE FROM {table_name};")

    else:
      cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
      """)
      tables = cursor.fetchall()
      for (table_name,) in tables:
        cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")

    conn.commit()

def close_connection():
  cursor.close()
  conn.close()

if __name__ == '__main__':
  create_tables_from_file(os.path.join("AniAlert", "db", "schema_postgres.sql"))
  print_table_contents()
  # delete_all_data()
  # print_table_contents()
  close_connection()
