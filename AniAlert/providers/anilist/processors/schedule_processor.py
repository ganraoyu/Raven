YEAR = 2025
SEASON = "SUMMER"

import requests
import json

from AniAlert.providers.anilist.query_loader import load_graphql_query

query = load_graphql_query('queries/schedule_query.graphql')

def build_variables():
  return {
  "page": 1,
  "perPage": 50,
  "seasonYear": YEAR,
  "season": SEASON,
  "type": "ANIME"
}

def get_schedule() -> list[dict]:
  variables = build_variables()

  response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})

  if response.status_code != 200:
    raise Exception(f"HTTP Error {response.status_code}: {response.text}")

  result = response.json()

  if "errors" in result:
    raise Exception(f"GraphQL Error: {json.dumps(result['errors'], indent=2)}")
  
  animes_list = []
  
  medias = result['data']['Page']['media']

  for media in medias:
    title = media['title'].get('english') or media['title'].get('romaji')
    start_date = media.get('startDate', None)
    end_date = media.get('endDate', None)

    nodes = media.get('airingSchedule', None).get('nodes'   , None)
    
    if nodes:
      for node in nodes:
        node['time_until_airing'] = node.pop('timeUntilAiring', None)
        node['airing_at_unix'] = node.pop('airingAt', None)
    
    animes_list.append({
      'title': title,
      'start_date': start_date,
      'end_date': end_date,
      'airing_schedule': nodes,
      })

  return animes_list

if __name__ == '__main__':
  animes = get_schedule()
  print(json.dumps(animes, indent=2, ensure_ascii=False))
