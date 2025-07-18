from typing import List, Optional
import json

import discord
from discord.ext import commands
from discord import app_commands, Interaction

from AniAlert.utils.builders.embed_builder import build_anime_notify_list_embed
from AniAlert.utils.discord_commands.interaction_helper import get_user_and_guild_ids
from AniAlert.db.database import get_db_connection

class CheckNotifyListCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot    
    self.conn = get_db_connection()
    self.cursor = self.conn.cursor()
    
  def cog_unload(self):
    self.cursor.close()
    self.conn.close()

  @app_commands.command(name='list', description='Check notify list')
  @app_commands.describe(
    id='Choose the anime to view its notify list',
    full_list='Show all upcoming episodes instead of just the next one'
  )
  @app_commands.choices(
    full_list=[
      app_commands.Choice(name='True', value='True'),
      app_commands.Choice(name='False', value='False')
    ]
  )
  async def check_notify_list(
    self, 
    interaction: Interaction,
    id: Optional[int] = None,
    full_list: Optional[str] = 'False'
  ):
    await interaction.response.defer(ephemeral=True)
    user_id, guild_id = self._get_user_guild_ids(interaction)

    results = self._fetch_notify_list(user_id, guild_id, id)

    if not results:
      await interaction.followup.send("⚠️ Your notify list is empty.", ephemeral=True)
      return

    embeds = self._create_notify_list_embeds(results, full_list)[:10]
    await interaction.followup.send(embeds=embeds, ephemeral=True)

  def _get_user_guild_ids(self, interaction: Interaction) -> tuple[int, int]:
    user_id, guild_id = get_user_and_guild_ids(interaction)
    return int(user_id), int(guild_id)

  def _fetch_notify_list(self, user_id: int, guild_id: int, id: int = None) -> List[tuple]:
    if id == None:
      query = 'SELECT * FROM anime_notify_list WHERE user_id = ? AND guild_id = ?'
      self.cursor.execute(query, (user_id, guild_id))
      return self.cursor.fetchall()
    elif id != None:
      query = 'SELECT * FROM anime_notify_list WHERE user_id = ? AND guild_id = ? AND id = ?'
      self.cursor.execute(query, (user_id, guild_id, id))
      return self.cursor.fetchall()

  def _get_notify_list_embed(self, anime, full_list: str = 'False') -> discord.Embed:
    id_ = anime[0]
    anime_name = anime[5]
    image = anime[9]

    if full_list == 'True':
      episodes = json.loads(anime[10])
    else:
      episodes = [{
        "episode": anime[6],
        "airingAt_iso": anime[8]
      }]

    return build_anime_notify_list_embed(anime_name, id_, episodes[:10], image)

  def _create_notify_list_embeds(self, results: List[tuple], full_list: str = 'False') -> List[discord.Embed]:
      embeds = [] 

      for anime in results:
        embed = self._get_notify_list_embed(anime, full_list)
        embeds.append(embed)

      return embeds
      