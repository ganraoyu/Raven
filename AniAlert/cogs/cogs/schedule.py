import discord

from discord.ext import commands
from discord import app_commands, Interaction

from AniAlert.services.anime_service import get_schedule

class ScheduleCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='schedule', description='Get current seasonal airing schedule')
  async def schedule(self, interaction: Interaction,):
    await interaction.response.defer(ephemeral=True)