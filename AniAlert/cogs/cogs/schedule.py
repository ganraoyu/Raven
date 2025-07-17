from discord.ext import commands
from discord import app_commands, Interaction

from AniAlert.services.anime_service import get_schedule
from AniAlert.utils.builders.embed_builder import build_schedule_embed
from AniAlert.utils.time_helper import get_today_time, get_end_of_week_unix

class ScheduleCog(commands.Cog):
  def __init__(self, bot, cursor, conn):
    self.bot = bot
    self.cursor = cursor
    self.conn = conn

  @app_commands.command(name='schedule', description='Get current seasonal airing schedule')
  @app_commands.describe(day_range='Choose between today\'s schedule or the full week')
  @app_commands.choices(
    day_range=[
      app_commands.Choice(name='Today', value='today'),
      app_commands.Choice(name='This Week', value='week')
    ]
  )
  async def schedule(
    self, 
    interaction: Interaction,
    day_range: app_commands.Choice[str] = None
    ):
    await interaction.response.defer(ephemeral=True)

    choice = day_range.value if day_range else 'today'

    _, today_unix_midnight, current_unix_time = get_today_time()

    if choice == 'today':
      tomorrow_unix = today_unix_midnight + 86400  # 1 day in seconds
      time_stamp = (today_unix_midnight, tomorrow_unix)
    elif choice == 'week':
      end_of_week_unix = get_end_of_week_unix()
      time_stamp = (today_unix_midnight, end_of_week_unix)


    select_query = '''
      SELECT * FROM seasonal_schedule WHERE airing_at_unix BETWEEN ? AND ?
    '''

    self.cursor.execute(select_query, time_stamp )
    rows = self.cursor.fetchall()
    embeds = []

    for row in rows:
      anime_name = row[1]
      episode_number = row[2]
      airing_at_unix = row[3]
      image = row[6]

      airing_schedule = [{'episode': episode_number, 'time_until_airing': airing_at_unix - current_unix_time}]
      embed = build_schedule_embed(anime_name, airing_schedule, image)
      embeds.append(embed)

    await interaction.followup.send(embeds=embeds[:10], ephemeral=True)




