from datetime import datetime

def get_season(month: int) -> str:
  if month in [1, 2, 3]:
    return "WINTER"
  elif month in [4, 5, 6]:
    return "SPRING"
  elif month in [7, 8, 9]:
    return "SUMMER"
  else:
    return "FALL"

def get_current_time():
  current_datetime = datetime.now()
  
  current_year = current_datetime.year
  current_month = current_datetime.month
  
  current_season = get_season(current_month)

  return current_year, current_season

def get_season_year():
  return get_current_time()
