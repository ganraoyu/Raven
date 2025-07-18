from discord.ext import commands
from discord import app_commands, Interaction

from AniAlert.utils.discord_commands.interaction_helper import get_user_and_guild_ids
from AniAlert.db.database import get_db_connection

class ClearNotifyListCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.conn = get_db_connection()
    self.cursor = self.conn.cursor()

  def cog_unload(self):
    self.cursor.close()
    self.conn.close()
    
  @app_commands.command(name='clear_list')
  async def clear(self, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id, guild_id = get_user_and_guild_ids(interaction)
    user_id, guild_id = int(user_id), int(guild_id)

    try:
      deleted_count = self._delete_notify_list(user_id, guild_id)
    except Exception as e:
      await interaction.followup.send(
        "⚠️ An error occurred while clearing your notify list.",
        ephemeral=True
      )
      print(f"[ERROR] clear_list command: {e}")
      return

    if deleted_count == 0:
      await interaction.followup.send(
        "⚠️ Your notify list is empty.", ephemeral=True
      )
      return

    await interaction.followup.send(
      content=(
        "✅ **All your anime notifications have been successfully removed!**\n"
        "You will no longer receive alerts for any anime from your notify list."
      ),
      ephemeral=True
    )

  def _delete_notify_list(self, user_id: int, guild_id: int) -> int:
    query = 'DELETE FROM anime_notify_list WHERE guild_id = ? AND user_id = ?'
    self.cursor.execute(query, (guild_id, user_id))
    self.conn.commit()
    return self.cursor.rowcount
