from discord.ext import commands
from discord import app_commands, Interaction

from AniAlert.services.anime_service import get_schedule
from AniAlert.utils.builders.embed_builder import build_schedule_embed

class ScheduleCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='schedule', description='Get current seasonal airing schedule')
  async def schedule(self, interaction: Interaction,):
    await interaction.response.defer(ephemeral=True)

    animes = get_schedule()

    embeds = []

    for anime in animes:
      anime_name = anime['title']
      airing_schedule = anime['airing_schedule']
      image = anime['image']

      embed = build_schedule_embed(anime_name, airing_schedule, image)
      embeds.append(embed)

    await interaction.followup.send(embeds=embeds[:10], ephemeral=True)




