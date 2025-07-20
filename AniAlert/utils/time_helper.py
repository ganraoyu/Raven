from datetime import datetime, timezone
import datetime

def get_today_time():
  today = datetime.date.today()
  current_time = datetime.datetime.now()
  current_unix_time = int(current_time.timestamp())
  midnight = datetime.datetime.combine(today, datetime.time.min)
  today_unix_midnight = int(midnight.timestamp())

  return today, today_unix_midnight, current_unix_time

def get_next_day_unix():
  today = datetime.date.today()
  next_day = today + datetime.timedelta(days=1)

  start_of_day = datetime.datetime.combine(next_day, datetime.time.min)  # 00:00:00
  end_of_day = datetime.datetime.combine(next_day, datetime.time(hour=23, minute=59, second=59))  # 23:59:59

  start_unix = int(start_of_day.timestamp())
  end_unix = int(end_of_day.timestamp())

  return start_unix, end_unix

def get_end_of_week_unix() -> int:
  today = datetime.date.today()
  days_ahead = 6 - today.weekday() 
  end_of_week_date = today + datetime.timedelta(days=days_ahead)
  end_of_week_datetime = datetime.datetime.combine(end_of_week_date, datetime.time.max)
  end_of_week_datetime = end_of_week_datetime.replace(tzinfo=timezone.utc)
  return int(end_of_week_datetime.timestamp())

def get_end_of_next_week_unix ():
  today = datetime.date.today()

  days_until_next_monday = (7 - today.weekday()) % 7 + 0
  next_monday = today + datetime.timedelta(days=days_until_next_monday)
  next_sunday = next_monday + datetime.timedelta(days=6)

  start_of_week = datetime.datetime.combine(next_monday, datetime.time.min)
  end_of_week = datetime.datetime.combine(next_sunday, datetime.time(hour=23, minute=59))

  start_unix = int(start_of_week.timestamp())
  end_unix = int(end_of_week.timestamp())

  return start_unix, end_unix

def convert_unix(seconds: int) -> str:
  if seconds is None:
    return "unknown"

  days = seconds // 86400
  hours = (seconds % 86400) // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60

  parts = []
  if days > 0:
    parts.append(f"{days}d")
  if hours > 0:
    parts.append(f"{hours}h")
  if minutes > 0:
    parts.append(f"{minutes}m")
  if seconds > 0 or not parts:
    parts.append(f"{seconds}s")

  return " ".join(parts)

def convert_iso(iso_time: str) -> str:
  if not iso_time:
    return "unknown"

  if iso_time.endswith('Z'):
    iso_time = iso_time[:-1] + '+00:00'

  dt = datetime.datetime.fromisoformat(iso_time)

  if dt.tzinfo is None:
    dt = dt.replace(tzinfo=timezone.utc)

  now = datetime.datetime.now(timezone.utc)
  delta = dt - now

  if delta.total_seconds() <= 0:
    return "soon"

  days = delta.days
  hours = delta.seconds // 3600
  minutes = (delta.seconds % 3600) // 60
  seconds = delta.seconds % 60

  parts = []
  if days > 0:
    parts.append(f"{days} day{'s' if days != 1 else ''}")
  if hours > 0:
    parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
  if minutes > 0:
    parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
  if seconds > 0 and not parts:
    parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

  return "in " + " ".join(parts) if parts else "soon"
