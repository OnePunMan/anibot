import requests, json, logging

ANILIST_URL = 'https://graphql.anilist.co'

def getAnime(name: str):
    querySearch = '''
    query ($searchInput: String) {
        Page (page: 1, perPage: 20) {
            media (search: $searchInput, sort: POPULARITY_DESC) {
                id
                description (asHtml: false)
                status
                type
                averageScore
                episodes
                volumes
                format
                siteUrl
                isAdult
                coverImage {
                    medium
                }
                title {
                    romaji
                    english
                    native
                }
            }
        }
    }
    '''

    # Query variable
    variables = {
        'searchInput': name
    }

    # Make the HTTP Api request
    response = requests.post(ANILIST_URL, json={'query': querySearch, 'variables': variables})
    if not response.ok:
        logging.error(f"Failed to search anime {name}. Error: {response.text}")
        return []

    result = json.loads(response.text)["data"]["Page"]["media"]
    logging.info(f'Anime results returned for query "{name}": {len(result)}')
    return result

def getUserInfo(token: str) -> (int, str):
    query = '''
    query {
        Viewer {
            name
            id
        }
    }
    '''

    variables = dict()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(ANILIST_URL, headers=headers ,json={'query': query, 'variables': variables})
    if not response.ok:
        logging.error(f"Failed to get user info. Error: {response.text}")
        return None

    result = response.json()['data']['Viewer']
    logging.info(f"Got user info from AniList: {result}")

    
    return (result['id'], result['name'])
    

# Get's the list of status "WATCHING"
def getAnimeList(user_id: int) -> list:
    query = '''
    query ($userId: Int) {
        Page {
            mediaList (userId: $userId, status: CURRENT, type: ANIME){
                progress
                media {
                    id
                    episodes
                    title {
                        romaji
                        english
                        native
                    }
                }
            }
        }
    }
    '''

    variables = {
        "userId": int(user_id)
    }

    response = requests.post(ANILIST_URL, json={'query': query, 'variables': variables})
    if not response.ok:
        logging.error(f"Failed to get user's anime list. Error: {response.text}")
        return []

    result = response.json()['data']['Page']['mediaList']
    logging.info(f"Got user info from AniList: {result}")

    return result

def increaseProgress(access_token: str, media_id: int):
    pass