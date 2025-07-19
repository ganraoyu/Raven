import requests
import json

def search_anime_by_image(image_bytes, filename='image.png'):
    response = requests.post(
        'https://api.trace.moe/search',
        files={'image': (filename, image_bytes)}
    )
    response.raise_for_status()
    data = response.json()
    return data['result'][0]

def get_anime_title(id: int):
    query = '''
    query ($id: Int) {
      Media(id: $id, type: ANIME) {
        siteUrl
        title {
          romaji
          english
        }
      }
    }
    '''

    variables = {'id': id}

    response = requests.post(
        'https://graphql.anilist.co',
        json={'query': query, 'variables': variables}
    )
    response.raise_for_status()
    
    data = response.json()
    title = data['data']['Media']['title']

    link = data['data']['Media']['siteUrl']
    english = title['english']
    romaji = title['romaji']

    return {
      'english': english,
      'romaji': romaji,
      'link': link
    }


if __name__ == '__main__':
    with open('test.png', 'rb') as f:
        image_bytes = f.read()

    data = search_anime_by_image(image_bytes)
    title = get_anime_title(data['anilist'])
    print(json.dumps(data, indent=2))
    print(title)
