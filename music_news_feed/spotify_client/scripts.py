from base64 import b64encode
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
import requests
import json
from artists.models import Artists

CLIENT_ID = 'd0b4fdc35c2a4c13b34a489a4c1ad496'
CLIENT_SECRET = '5fc4a2aae70e4532a81042001b3c88ec'
BASE_URL = 'https://api.spotify.com/v1/'


def get_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    data = urlencode({'grant_type': 'client_credentials'}).encode('ascii')
    headers = {'Authorization': b'Basic ' + b64encode((client_id + ':' + client_secret).encode('utf-8'))}
    response = urlopen(Request(url, data, headers))  # , cafile=cafile)
    return json.load(response)['access_token']


def get_auth_headers():
    return {
        'Authorization': 'Bearer ' + get_token(CLIENT_ID, CLIENT_SECRET)
    }


def build_url(url):
    return urljoin(BASE_URL, url)


def search_artist(query):
    params = {
        'q': query,
        'type': 'artist',
    }
    response = requests.get(build_url('search'), params=params, headers=get_auth_headers())
    resp_objects = json.loads(response.content.decode())['artists']['items']
    answer = []
    for obj in resp_objects:
        img_url = None
        max_height = 0
        for image in obj['images']:
            if image['height'] > max_height:
                img_url = image['url']
                max_height = image['height']
        answer.append({
            'name': obj['name'],
            'img_url': img_url,
            'genres': obj['genres'],
            'spotify_id': obj['id'],
            'is_in_library': False if Artists.get_or_none(spotify_id=obj['id']) is None else True
        })
    return answer


def get_something():
    url = 'artists/08td7MxkoHQkXnWAYD8d6Q'
    response = requests.get(build_url(url), headers=get_auth_headers())
    return response.content.decode()


def get_artist_info(artist_spotify_id):
    response = requests.get(build_url('artists/' + artist_spotify_id), headers=get_auth_headers())
    artist_obj = json.loads(response.content.decode())
    img_url = None
    max_height = 0
    for image in artist_obj['images']:
        if image['height'] > max_height:
            img_url = image['url']
            max_height = image['height']
    return {
        'name': artist_obj['name'],
        'img_url': img_url,
        'spotify_id': artist_obj['id'],
        'genres': json.dumps(artist_obj['genres'])
    }


def get_artists_albums(artist_spotify_id):
    params = {
        'limit': 50
    }
    response = requests.get(
        build_url('artists/{}/albums'.format(artist_spotify_id)),
        headers=get_auth_headers(),
        params=params
    )


def get_track_info():
    pass