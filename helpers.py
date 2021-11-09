"""Helper Functions for Spotiflavor"""

from re import M
from models import db, Track, Album, Artist, Genre, PlaylistTrack, TrackArtist, TrackGenre

def get_spotify_track_ids(items):
    """Create list of found track ids from Spotify"""

    spot_track_ids = []
    for item in items:
        spot_track_ids.append(item['track']['id'])
    return spot_track_ids

def process_track_search(found_tracks):
    """Check if db has each spotify track id
        if spotify_track_id not found, create entry return id
        if spotify_track_id is found, return id
        return a list of ids (both found and created) from search
    """

    track_ids = []
    for track in found_tracks:
        #Check if in db
        track_exists = Track.query.filter(Track.spotify_track_id==track['track']['id']).first()
        #If yes, get id, append to track_ids[]
        if track_exists:
            track_ids.append(track_exists.id)
        #If no, populate db, append id to track_ids[]
        else:
            new_track = Track(
                spotify_track_id=track['track']['id'],
                name=track['track']['name'],
                popularity=track['track']['popularity'],
                spotify_track_url=track['track']['external_urls']['spotify'],
                spotify_track_uri=track['track']['uri'],
                preview_url=track['track']['preview_url'],
                release_year=track['track']['album']['release_date'][:4],
                duration=track['track']['duration_ms'])
            
            # check if album in db, if so connect to track else create and connect
            album = Album.query.filter(Album.spotify_album_id==track['track']['album']['id']).first()
            if album:
                new_track.album_id = album.id
            else:
                new_album = Album(
                    spotify_album_id = track['track']['album']['id'],
                    name = track['track']['album']['name'],
                    image = track['track']['album']['images'][2]['url']
                )
                Album.insert(new_album)
                new_track.album_id = new_album.id
            Track.insert(new_track)
            track_ids.append(new_track.id)

        if track_exists:
             track_id = track_exists.id
        else:
            track_id = new_track.id

        #loop through artists
        for artist in track['track']['artists']:
            #Check if in db
            artist_exists = Artist.query.filter(Artist.spotify_artist_id==artist['id']).first()
            #If artist in db and track is not in db
            if artist_exists and not track_exists:
                #if exists connect to track
                new_track_artist = TrackArtist(track_id=track_id, artist_id=artist_exists.id)
                db.session.add(new_track_artist)
                db.session.commit()
            #If artist in db and track track is in db: do nothing
            elif artist_exists:
                pass
            #Artist not in db
            else:
                new_artist = Artist(
                    spotify_artist_id=artist['id'],
                    name=artist['name']
                )
                Artist.insert(new_artist)
                new_track_artist = TrackArtist(track_id=track_id, artist_id=new_artist.id)
                db.session.add(new_track_artist)
                db.session.commit()
            

            #Genre
        
        
        

    return track_ids

def parse_search(obj):
    """parse a returned search object and return the values"""

    href = obj['href']
    items = obj['items']
    limit = obj['limit']
    next = obj['next']
    offset = obj['offset']
    previous = obj['previous']
    total = obj['total']

    print('HREF', obj['href'])

    return {
        obj['href']
    }



def parse_tracks_items(obj):
    """Parse the object items of a search track request"""

    album = obj['album']
    artists = obj['artists']
    available_markets = obj['available_markets']
    disc_number = obj['disc_number']
    duration_ms = obj['duration_ms']
    explicit = obj['explicit']
    external_ids = obj['external_ids']
    external_urls = obj['external_urls']
    href = obj['href']
    id = obj['id']
    is_local = obj['is_local']
    name = obj['name']
    popularity = obj['popularity']
    preview_url = obj['preview_url']
    track_number = obj['track_number']
    type = obj['type']
    uri = obj['uri']

def parse_album_items(obj):
    """Parse the object items of a search album request"""

    album_type = obj['album_type']
    artists = obj['artists']
    available_markets = obj['available_markets']
    external_urls = obj['external_urls']
    href = obj['href']
    id = obj['id']
    images = obj['images'][0]['url']
    images = obj['images'][0]['height']
    images = obj['images'][0]['width']
    name = obj['name']
    release_date = obj['release_date']
    release_date_precision = obj['release_date_precision']
    total_tracks = obj['total_tracks']
    type = obj['type']
    uri = obj['uri']

def parse_artist_items(obj):
    """Parse the object items of a search artist"""


    external_urls = obj['external_urls']
    href = obj['href']
    id = obj['id']
    name = obj['name']
    type = obj['type']
    uri = obj['uri']
