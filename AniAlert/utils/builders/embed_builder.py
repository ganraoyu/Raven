import discord
from typing import List, Tuple
from ..time_helper import convert_iso, convert_unix

def get_anime_variables(anime: dict) -> dict:
  title = anime.get('title') or 'Unknown Title'
  synopsis = anime.get('synopsis') or 'No synopsis available.'
  studios = str(anime.get('studios') or 'N/A')
  show_type = str(anime.get('show_type') or 'N/A')
  rating = str(anime.get('average_rating') or 'N/A')
  episodes = str(anime.get('episodes') or 0)
  status = str(anime.get('status') or 'N/A').upper()
  ranking = str(anime.get('ranking') or 'N/A')
  genres = str(anime.get('genres') or 'Unknown')
  image = anime.get('image')
  time_until_airing = str(anime.get('time_until_airing') or 'N/A')
  airingAt_iso = str(anime.get('airingAt_iso') or 'N/A')
  remaining_anime_titles = anime.get('remaining_anime_titles' or 'N/A')

  return {
    'title': title,
    'synopsis': synopsis,
    'studios': studios,
    'show_type': show_type,
    'rating': rating,
    'episodes': episodes,
    'status': status,
    'ranking': ranking,
    'genres': genres,
    'image': image,
    'time_until_airing': time_until_airing,
    'airingAt_iso': airingAt_iso,
    'remaining_anime_titles': remaining_anime_titles,
  }

def build_search_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'🎬 {vars["title"]}',
    description=vars['synopsis'],
    color=discord.Color.purple()
  )
  embed.add_field(name='📺 Type', value=vars['show_type'], inline=True)
  embed.add_field(name='⭐ Rating', value=vars['rating'], inline=True)
  embed.add_field(name='🎞️ Episodes', value=vars['episodes'], inline=True)
  embed.add_field(name='🗓️ Status', value=vars['status'], inline=True)
  embed.add_field(name='🏆 Rank', value=vars['ranking'], inline=True)
  embed.add_field(name='🎭 Genres', value=vars['genres'], inline=True)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  embed.set_footer(text="AniAlert • Search Results")
  return embed

def build_seasonal_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'🎬 {vars["title"]}',
    description=vars['synopsis'],
    color=discord.Color.blue()
  )

  embed.add_field(name='📺 Type', value=vars['show_type'], inline=True)
  embed.add_field(name='⭐ Rating', value=vars['rating'], inline=True)
  embed.add_field(name='🎞️ Episodes', value=vars['episodes'], inline=True)
  embed.add_field(name=f"⏰ Episode {int(vars['episodes']) + 1} airs in", value=vars['time_until_airing'], inline=True)
  embed.add_field(name='🎬 Studios', value=vars['studios'], inline=True)
  embed.add_field(name='🎭 Genres', value=vars['genres'], inline=True)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  embed.set_footer(text="AniAlert • Seasonal Anime")
  return embed

def build_add_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'🎬 {vars["title"]}',
    color=discord.Color.green()
  )

  embed.add_field(name=f"Episode {int(vars['episodes']) + 1} in", value=vars['time_until_airing'], inline=False)
  embed.add_field(name='🗓️ Airing at', value=vars['airingAt_iso'], inline=False)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  embed.set_footer(text="AniAlert • Anime Added") 
   
  return embed

def build_remove_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'❌ Removed: {vars["title"]}',
    color=discord.Color.red()
  )

  embed.set_footer(text="AniAlert • Anime Removed")
  return embed

def build_anime_notify_list_embed(anime_name: str, id: int, episodes: list[dict], image: str) -> discord.Embed:
  embed = discord.Embed(
    title=f'🎬 {anime_name} (ID: {id})',
    color=discord.Color.dark_blue()
  )
  
  for ep in episodes:
    episode_num = ep.get('episode')
    air_time = convert_iso(ep.get('airingAt_iso'))
    embed.add_field(
      name=f'Episode {episode_num} airs in',
      value=air_time,
      inline=False
    )

  embed.set_thumbnail(url=image)  
  embed.set_footer(text="AniAlert • Notification List")
  return embed

def build_anime_airing_notification_embed(anime_name: str, episode: int, image_url: str, user_id: str) -> discord.Embed:
  embed = discord.Embed(
    title=f'📢Episode {episode} Aired: {anime_name}',
    description=f'<@{user_id}> A new episode just dropped — go check it out!',
    color=discord.Color.dark_blue()
  )
  embed.set_thumbnail(url=image_url)
  embed.set_footer(text="AniAlert • Airing Notification")
  return embed

def build_random_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)
  
  embed = discord.Embed(
    title=f'🎲 Random Anime: {vars["title"]}',
    description=vars['synopsis'],
    color=discord.Color.random()
  )
  
  embed.add_field(name='📺 Type', value=vars['show_type'], inline=True)  
  embed.add_field(name='⭐ Rating', value=vars['rating'], inline=True)
  embed.add_field(name='🎞️ Episodes', value=vars['episodes'], inline=True)
  embed.add_field(name='🗓️ Status', value=vars['status'], inline=True)
  embed.add_field(name='🎬 Studios', value=vars['studios'], inline=True)
  embed.add_field(name='🎭 Genres', value=vars['genres'], inline=True)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  embed.set_footer(text="AniAlert • Random Anime Generator")
  return embed

def build_guess_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    color=discord.Color.dark_magenta()
  )

  embed.set_image(url=vars['image'])

  return embed

def build_schedule_embed(
  anime_name: str,
  airing_schedule: list[dict],
  image_url: str,
  schedule_label: str = None
) -> discord.Embed :
  embed = discord.Embed(
    title=f'🎬 {anime_name}',
    color=discord.Color.dark_blue()
  )
 
  for ep in airing_schedule:
    episode_num = ep.get('episode')
    time_until_airing = ep.get('time_until_airing')

    if time_until_airing is None:
      continue 
    
    formatted_time = convert_unix(time_until_airing)
    if time_until_airing > 0:
      embed.add_field(
      name=f'Episode {episode_num} airs in',
      value=formatted_time,
      inline=False
    )
    elif time_until_airing < 0:
      embed.add_field(
      name=f'Episode {episode_num} already aired',
      value=f'{formatted_time} ago',
      inline=False
    )
      
  embed.set_thumbnail(url=image_url)
  if schedule_label:
    embed.set_footer(text=schedule_label)

  return embed

def build_anime_by_image_builder(
  anime_name: str, 
  episode: int,
  similarity: float,
  start_time: int,
  end_time: int, 
  link: str,
  image: str,
) -> discord.Embed:
  def format_time(seconds: float) -> str:
    total_seconds = int(seconds)
    minutes, secs = divmod(total_seconds, 60)
    return f'{minutes}:{secs:02}'
  
  embed = discord.Embed(
    title=f"🎬 {anime_name}",
    color=discord.Color.dark_blue()
  )

  embed.add_field(name="📺 Episode", value=str(episode), inline=True)
  embed.add_field(name="⏰ Timestamp", value=f"{format_time(start_time)} - {format_time(end_time)}", inline=True)
  embed.add_field(name="🔗 AniList Link", value=f"[Click here to view]({link})", inline=True)

  embed.set_footer(text="AniAlert • Search Image")
  embed.set_image(url=image)

  return embed

