import discord

from discord.ext import commands
from discord import app_commands, Interaction
from AniAlert.services.anime_service import get_anime_by_image
from AniAlert.utils.builders.embed_builder import build_anime_by_image_builder


class SearchAnimeByImage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='search_image', description='Search anime episode by image')
  @app_commands.describe(image="Attach an image")
  async def search_image(self, interaction: discord.Interaction, image: discord.Attachment):
    await interaction.response.defer()

    image_bytes = await image.read()
    result, titles = get_anime_by_image(image_bytes)

    episode = result['episode']
    similarity = result['similarity']
    anime_image = result['image']
    start_time = result['from']
    end_time = result['to']

    title = titles['english']
    link = titles['link']

    embed = build_anime_by_image_builder(title, episode, similarity, start_time, end_time, link, anime_image)

    await interaction.followup.send(embed=embed, ephemeral=True)