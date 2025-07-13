import requests
import json
import datetime
from AniAlert.utils.time_converter import convert_unix
from AniAlert.utils.common_genres_tags import get_common_genres_tags

common_genres, common_tags = get_common_genres_tags()

query = '''
query($search: String){
  Media(search: $search, type: ANIME){
    id,
    title{
      romaji,
      english
    },
    genres,
    tags{
      name
    },
    airingSchedule(notYetAired: true){
      nodes{
        airingAt,
        timeUntilAiring,
        episode
      }
    },
    averageScore,
    rankings {
      rank
      type
      allTime
      context
      season
      year
    }
    status
  }
}
'''

def _extract_episodes_list(airing_nodes):
  episode_list = []
  for node in airing_nodes:
    airing_at_unix = node.get('airingAt', 0)
    airing_at_iso = datetime.datetime.utcfromtimestamp(airing_at_unix).strftime("%Y-%m-%dT%H:%M:%S") if airing_at_unix else None
    time_until_airing = convert_unix(node.get('timeUntilAiring', 0))
    episode = node.get('episode', 0)

    episode_list.append({
      'airingAt_unix': airing_at_unix,
      'airingAt_iso': airing_at_iso,
      'time_until_airing': time_until_airing,
      'episode': episode
    })
  return episode_list

def search_anime_anilist(search):
    response = requests.post(
        'https://graphql.anilist.co',
        json={'query': query, 'variables': {'search': search}}
    )
    data = response.json()

    nodes = data['data']['Media']['airingSchedule']['nodes']

    for node in nodes:
      node['airingAt_unix'] = node['airingAt']
      node['airingAt_iso'] = datetime.datetime.utcfromtimestamp(node['airingAt_unix']).strftime("%Y-%m-%dT%H:%M:%S")
      node['time_until_airing'] = convert_unix(node['timeUntilAiring'])
    
    filtered_tags = []
    filtered_genres = []

    for genre in data['data']['Media']['genres']:
       if genre in common_genres:
          filtered_genres.append(genre)

    for tag in data['data']['Media']['tags']:
      if tag['name'] in common_tags:
        filtered_tags.append(tag['name']) 
    
    data['episode_list'] = _extract_episodes_list(nodes)

    data['data']['Media']['genres'] = filtered_tags + filtered_genres
    return data

if __name__ == '__main__':
  response = search_anime_anilist('One Piece')
  print(json.dumps(response, indent=2, ensure_ascii=False))
