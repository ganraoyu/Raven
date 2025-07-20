from discord.ext import commands
from discord import app_commands, Interaction
from AniAlert.utils.builders.embed_builder import build_remove_anime_embed
from AniAlert.db.database import get_db_connection, get_placeholder

placeholder = get_placeholder()

class RemoveAnimeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.conn = get_db_connection()
    self.cursor = self.conn.cursor()

  def cog_unload(self):
    self.cursor.close()
    self.conn.close()

  def _fetch_notify_list(self, id: int):
    query = f'SELECT * FROM anime_notify_list WHERE id = {placeholder}'
    self.cursor.execute(query, (id,))
    return self.cursor.fetchone()

  @app_commands.command(name='remove_anime', description='Remove animes from notify list')
  @app_commands.describe(id='Enter anime ID to remove')
  async def remove_anime(self, interaction: Interaction, id: int):
    await interaction.response.defer(ephemeral=True)
    try:
      result = self._fetch_notify_list(id)
      if not result:
        await interaction.followup.send(f"⚠️ No anime found with ID `{id}`.", ephemeral=True)
        return
      
      anime_dict = {
        'id': result[0],
        'guild_id': result[1],
        'guild_name': result[2],
        'user_id': result[3],
        'user_name': result[4],
        'title': result[5],
        'episode': result[6],
        'unix_air_time': result[7],
        'iso_air_time': result[8],
        'image': result[9]
      }

      embed = build_remove_anime_embed(anime_dict)

      delete_query = f'DELETE FROM anime_notify_list WHERE id = {placeholder}'
      self.cursor.execute(delete_query, (id,))

      self.conn.commit()

      await interaction.followup.send(embed=embed, ephemeral=True)
      
    except Exception as e:
      await interaction.followup.send("⚠️ An error occurred while trying to remove the anime.", ephemeral=True)
      print(f"[ERROR] remove_anime: {e}")
