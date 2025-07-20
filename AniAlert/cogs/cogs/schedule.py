from datetime import datetime

from discord.ext import commands
from discord import app_commands, Interaction

from AniAlert.services.anime_service import get_schedule
from AniAlert.utils.builders.embed_builder import build_schedule_embed
from AniAlert.utils.time_helper import get_today_time, get_end_of_week_unix, get_end_of_next_week_unix, get_next_day_unix
from AniAlert.db.database import get_db_connection, get_placeholder

placeholder = get_placeholder()


def _get_time_stamp(day_range):
  choice = day_range.value if day_range else 'today'
  _, today_unix_midnight, current_unix_time = get_today_time()

  if choice == 'today':
    tomorrow_unix = today_unix_midnight + 86400  # 1 day in seconds
    time_stamp = (today_unix_midnight, tomorrow_unix)
  elif choice == 'tomorrow':
    start_of_tomorrow, end_of_tomorrow = get_next_day_unix()
    time_stamp = (start_of_tomorrow, end_of_tomorrow)
  elif choice == 'week':
    end_of_week_unix = get_end_of_week_unix()
    time_stamp = (today_unix_midnight, end_of_week_unix)
  elif choice == 'next_week':
    start_of_week, end_of_week = get_end_of_next_week_unix()
    time_stamp = (start_of_week, end_of_week)

  return choice, current_unix_time, time_stamp

def _build_labels(time_stamp: tuple, choice: str):
  start_label = datetime.fromtimestamp(time_stamp[0]).strftime('%A, %B %d')
  end_label = datetime.fromtimestamp(time_stamp[1]).strftime('%A, %B %d')

  if choice == 'today':
    schedule_label = f"Schedule for {start_label}"
  else:
    schedule_label = f"Schedule for {start_label} - {end_label}"
  return schedule_label


def _fetch_schedule_rows(cursor, time_stamp):
  select_query = f'''
    SELECT * FROM seasonal_schedule WHERE airing_at_unix BETWEEN {placeholder} AND {placeholder}
  '''
  cursor.execute(select_query, time_stamp)
  return cursor.fetchall()


def _build_embed_with_times(rows, current_unix_time, schedule_label):
  embed_with_times = []
  for row in rows:
    anime_name = row[1]
    episode_number = row[2]
    airing_at_unix = row[3]
    image = row[6]

    time_until_airing = airing_at_unix - current_unix_time

    airing_schedule = [{
      'episode': episode_number,
      'time_until_airing': time_until_airing
    }]

    embed = build_schedule_embed(anime_name, airing_schedule, image, schedule_label)

    if embed.title or embed.description or embed.fields:
      embed_with_times.append((embed, time_until_airing))

  return embed_with_times


def _sort_embed(embed_with_times: list):
  sorted_list = sorted(embed_with_times, key=lambda x: x[1])
  sorted_embeds = [embed for embed, _ in sorted_list]
  return sorted_embeds


class ScheduleCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.conn = get_db_connection()
    self.cursor = self.conn.cursor()

  def cog_unload(self):
    self.cursor.close()
    self.conn.close()

  @app_commands.command(name='schedule', description='Get current seasonal airing schedule')
  @app_commands.describe(day_range='Choose between today\'s schedule or the full week')
  @app_commands.choices(
    day_range=[
      app_commands.Choice(name='Today', value='today'),
      app_commands.Choice(name='Tomorrow', value='tomorrow'),
      app_commands.Choice(name='This Week', value='week'),
      app_commands.Choice(name='Next Week', value='next_week')
    ]
  )
  async def schedule(
    self,
    interaction: Interaction,
    day_range: app_commands.Choice[str] = None
  ):
    await interaction.response.defer(ephemeral=True)

    try:
      choice, current_unix_time, time_stamp = _get_time_stamp(day_range)
      schedule_label = _build_labels(time_stamp, choice)
      rows = _fetch_schedule_rows(self.cursor, time_stamp)
      embed_with_times = _build_embed_with_times(rows, current_unix_time, schedule_label)
      sorted_embeds = _sort_embed(embed_with_times)

      if sorted_embeds:
        for i in range(0, len(sorted_embeds), 10):
          await interaction.followup.send(embeds=sorted_embeds[i:i+10], ephemeral=True)
      else:
        await interaction.followup.send(
          "⚠️ No more anime are currently airing today. Please try again later.",
          ephemeral=True
        )

    except Exception as e:
      print(f"[ERROR] schedule command: {e}")
      await interaction.followup.send(
        "⚠️ An error occurred while fetching the schedule. Please try again later.",
        ephemeral=True
      )
