from base64 import b64encode
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
import requests
import json
from artists.models import Artists
from albums.models import Albums, AlbumTypes
from tracks.models import Tracks

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


def best_image_url(images):
    img_url = None
    max_height = 0
    for image in images:
        if image['height'] > max_height:
            img_url = image['url']
            max_height = image['height']
    return img_url

def get_release_date(release_date, release_date_precision):
    if release_date_precision == 'day':
        return release_date
    elif release_date_precision == 'month':
        return release_date + '-01'
    else:
        return release_date + '-01-01'


def search_artist(user, query):
    if not query:
        return []
    params = {
        'q': query,
        'type': 'artist',
    }
    response = requests.get(build_url('search'), params=params, headers=get_auth_headers())
    resp_objects = json.loads(response.content.decode())['artists']['items']
    answer = []
    for obj in resp_objects:
        is_in_library = False
        artist = Artists.get_or_none(spotify_id=obj['id'])
        if artist and artist in user.artists_preferences.filter(status=True):
            is_in_library = True
        answer.append({
            'name': obj['name'],
            'img_url': best_image_url(obj['images']),
            'genres': obj['genres'],
            'spotify_id': obj['id'],
            'is_in_library': is_in_library
        })
    return answer


def get_artist_info(artist_spotify_id):
    response = requests.get(build_url('artists/' + artist_spotify_id), headers=get_auth_headers())
    artist_obj = json.loads(response.content.decode())
    return {
        'name': artist_obj['name'],
        'img_url': best_image_url(artist_obj['images']),
        'spotify_id': artist_obj['id'],
        'genres': json.dumps(artist_obj['genres'])
    }


def track_info(track_obj):
    return {
        'name': track_obj['name'],
        'artists': [x['id'] for x in track_obj['artists']],
        'track_number': track_obj['track_number'],
        'disc_number': track_obj['disc_number'],
        'duration_ms': track_obj['duration_ms'],
        'spotify_id': track_obj['id'],
        'preview_url': track_obj['preview_url']
    }


def get_several_albums(ids):
    params = {
        'ids': ','.join(ids)
    }
    response = requests.get(build_url('albums'), params=params, headers=get_auth_headers())
    resp_objects = json.loads(response.content.decode())['albums']
    answer = []
    for obj in resp_objects:
        answer.append({
            'name': obj['name'],
            'album_type': AlbumTypes.LP,
            'genres': json.dumps(obj['genres']),
            'spotify_id': obj['id'],
            'img_url': best_image_url(obj['images']),
            'release_date': get_release_date(obj['release_date'], obj['release_date_precision']),
            'artists': [x['id'] for x in obj['artists']],
            'tracks': [track_info(x) for x in obj['tracks']['items']]
        })
    return answer


def get_artists_albums(artist_spotify_id):
    params = {
        'limit': 20,
        'include_groups': 'album'
    }
    response = requests.get(
        build_url('artists/{}/albums'.format(artist_spotify_id)),
        headers=get_auth_headers(),
        params=params
    )
    album_objects = json.loads(response.content.decode())['items']
    answer = get_several_albums([x['id'] for x in album_objects])
    return answer


def add_tracks_for_album(album, tracks):
    for track in tracks:
        track_obj = Tracks.objects.create(
            name=track['name'],
            album=album,
            track_number=track['track_number'],
            disc_number=track['disc_number'],
            duration_ms=track['duration_ms'],
            spotify_id=track['spotify_id'],
            preview_url=track['preview_url']
        )
        for artist_sp_id in track['artists']:
            artist = Artists.get_or_none(spotify_id=artist_sp_id)
            if artist is not None:
                track_obj.artists.add(artist)


def add_albums_to_updates(user, artist, albums):
    for album in albums:
        album_obj = Albums.get_or_none(spotify_id=album['spotify_id'])
        if album_obj is None:
            album_obj = Albums.objects.create(
                name=album['name'],
                album_type=album['album_type'],
                genres=album['genres'],
                spotify_id=album['spotify_id'],
                img_url=album['img_url'],
                release_date=album['release_date']
            )
            add_tracks_for_album(album_obj, album['tracks'])
        album_obj.artists.add(artist)
        user.album_updates.get_or_create(album=album_obj)


def add_artist_to_user(artist_spotify_id, user):
    artist = Artists.get_or_none(spotify_id=artist_spotify_id)
    if artist is None:
        info = get_artist_info(artist_spotify_id)
        artist = Artists.objects.create(
            name=info['name'],
            img_url=info['img_url'],
            spotify_id=info['spotify_id'],
            genres=info['genres']
        )
        albums = get_artists_albums(info['spotify_id'])
        add_albums_to_updates(user, artist, albums)
    else:
        user.album_updates.add(Albums.objects.filter(artists=artist))
    user.artists_preferences.update_or_create(artist=artist, defaults={'status': True})
