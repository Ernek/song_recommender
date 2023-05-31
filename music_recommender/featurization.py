# Function to select track_uri ONLY 100 records for now
import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_features(df, N=1):
    """
    Gets song features from the Spotify API
    Args:
    df --> DataFrame containing music_data 
    N  --> Number of records to evaluate: default: N = 1
    """
    indexes = []
    audio_features = []
    track_popularity = []
    artist_genre = []
    artist_popularity = []
    album_popularity = []
    start = 0
    for row_index, row in df.iloc[0:N].iterrows():
        #print(row_index, row['track_track_uri'])
        track_uri = row['track_track_uri']
        artist_uri = row['track_artist_uri']
        album_uri = row['track_album_uri']
        if start == 0:
            keys = spotify.audio_features(tracks=track_uri)[0].keys()
        start += 1
    
        track_popularity.append(spotify.track(track_uri)['popularity'])
        
        indexes.append(row_index) 
        audio_features.append(spotify.audio_features(tracks=track_uri)[0].values())
        
        artist_results = spotify.artist(artist_uri)
        
        artist_genre.append(artist_results['genres'])
        artist_popularity.append(artist_results['popularity'])
        #print(artist_results['genres'], artist_results['popularity'])
        album_results = spotify.album(album_uri)
        album_popularity.append(album_results['popularity'])
        
        
    features_df = pd.DataFrame(audio_features, columns=keys)
    features_df['song_popularity'] = track_popularity
    features_df['artist_genre'] = artist_genre
    features_df['artist_popularity']  = artist_popularity
    features_df['album_popularity'] = album_popularity
    features_df['album_popularity'] = np.where(features_df['album_popularity'] == 0, features_df['artist_popularity'], features_df['album_popularity'])
    features_df['song_popularity'] = np.where(features_df['song_popularity'] == 0, features_df['artist_popularity'], features_df['song_popularity'])
    features_df['index'] = indexes
    features_df['artist_genre'] = features_df['artist_genre'].apply(lambda x: ' '.join([i.replace('-', ' ').replace('_', ' ') for i in x]))
    features_df.set_index('index', inplace=True)
    features_df.index.name = None
    features_df.drop(['type', 'id', 'track_href', 'analysis_url'], inplace=True, axis=1)
    # string_field = check_df.track_track_name.str.cat(" " + check_df.artist_genre)
    string_field = features_df.artist_genre
    string_field = string_field.replace({"r\&b": "rhythm blues"}, regex = True)
    string_field = string_field.replace({"[^A-Za-z ]+": ""}, regex = True)
    features_df['text'] = string_field
    
    return features_df

def merge_track_features_and_playlist(music_data, features_df, N=1):
    check_df = music_data.iloc[0:N].merge(features_df, how='left' , left_on = 'track_track_uri', right_on='uri')
    check_df.drop(['track_pos', 'uri', 'mode', 'playlist_duration_ms','playlist_num_albums','playlist_num_artists',  'track_artist_uri', 'track_album_uri', 'track_duration_ms','playlist_num_followers', 'playlist_num_edits', 'playlist_collaborative', 'playlist_modified_at', 'playlist_num_tracks'], inplace = True, axis=1)
    return check_df




