import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import skfuzzy as fuzz
import json
from math import floor
from copy import deepcopy
import os


root_path = os.getcwd()[:-5]
filepath = f"{root_path}/playlist_data/sampledata/"
filename = 'mpd.slice.0-999.json'
fpath_name = f"{filepath}{filename}"
with open(fpath_name) as data_file:    
    data = json.load(data_file)
    
playlists = pd.json_normalize(data['playlists'])

filename = 'song.slice.0-49999.csv'
fpath_name = f"{filepath}{filename}"

songs_df = pd.read_csv(fpath_name)
songs_df = songs_df.iloc[:,2:]
songs_num = songs_df.select_dtypes(include=np.number)

scaler = MinMaxScaler()
songs_num = scaler.fit_transform(songs_num)

def get_score(pred_songs, true_songs):
    
    pred_artists = {track['artist_name'] for track in pred_songs}
    true_artists = {track['artist_name'] for track in true_songs}
    pred_tracks = {track['track_name'] for track in pred_songs}
    true_tracks = {track['track_name'] for track in true_songs}

    artist_score = len(pred_artists.intersection(true_artists))
    track_score = len(pred_tracks.intersection(true_tracks))
    

    return [artist_score/(len(pred_artists)), track_score/(len(pred_tracks))]


def evaluate(suggestions, true=None, val_ratio=0.2, from_pid=False):
    
    """
    
    Args:
        
        suggestions (DataFrame or Series): Must have two columns 'pid' (playlist id) and 'tracks' (the suggested tracks).
        
        val_ratio (float): Ratio of songs in each playlist to withhold. Must be in between 0 and 1. When modeling the suggestions
            you should use only the first 1-val_ratio part of each playlist.
        
    Return:
    
        float: For each suggested song we get 1/2 each if artist/track is in the withheld tracks. The return is the
            average score per suggestion. Perfect score is 1 while no match at all gives 0.
    
    """
    
    if from_pid:
        val_songs = playlists.tracks.apply(lambda x: x[max(1,floor(len(x)*(1-val_ratio))):])
        total_score = suggestions

        scores = np.array([get_score(suggestions['tracks'][i], val_songs[i]) for i in suggestions.pid])
    else:
        
        n = len(suggestions)
        scores = np.array([get_score(suggestions[i], true[i]) for i in range(n)])
    
    result = {'artist_match_rate':np.mean(scores, axis=0)[0], 'track_match_rate':np.mean(scores,axis=0)[1]}
    
    return result

def evaluate_k_means_model(features,  playlists, n_suggestions=5):
    
    """
    
    Args:
        
        playlists (DataFrame): Must have a column 'tracks' which contains lists of songs (each song is a dictionary with keys
            'artist_name' and 'track_name').
            
        features (list) : The features that are used by the model, e.g ['danceability', 'beats']
        
        val_ratio (float): Ratio of songs in each playlist to withhold. Must be in between 0 and 1. When modeling the suggestions
            you should use only the first 1-val_ratio part of each playlist.
        
    Return:
    
        float: For each suggested song we get 1/2 each if artist/track is in the withheld tracks. The return is the
            average score per suggestion. Perfect score is 1 while no match at all gives 0.
    
    """
    
    partial_playlist = playlists.tracks.apply(lambda x: x[:max(1,floor(len(x)*(1-0.5)))])
    val_songs = playlists.tracks.apply(lambda x: x[max(1,floor(len(x)*(1-0.5))):])
    
    recs = []
    
    for i in range(len(playlists)):
                           
        playlist = playlists.tracks[i]
        uri_list = [track['track_uri'] for track in playlist]
        
        playlist = songs_num[[uri in uri_list for uri in songs_df['uri']]]
        playlist = playlist[features]
        
        # Predict the cluster
        clusters = model.predict(playlist)
        cluster = st.mode(clusters)

        # Suggest songs from the cluster
        
        recs.append(songs_df[model.labels_ == cluster].sample(n_suggestions).to_dict(orient='records'))
    
    recs_s = pd.Series(recs)

    return evaluate(recs_s, val_songs)







def evaluate_fuzzy_model(features,  playlists, n_suggestions=5, refinement=2):
    
    songs = songs_df[features]
    
    partial_playlist = playlists.tracks.apply(lambda x: x[:max(1,floor(len(x)*(1-0.5)))])
    val_songs = playlists.tracks.apply(lambda x: x[max(1,floor(len(x)*(1-0.5))):])
    
    # Train the fuzzy model
    num_clusters = 7
    cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(songs_num.T, num_clusters, m=1.00001, error=0.000005, maxiter=50000)
    all_songs_membership = fuzz.cluster.cmeans_predict(songs_num.T, cntr, 2, error=0.000005, maxiter=50000)[0]
    
    recs = []
    
    for i in range(len(playlists)):
                           
        playlist = playlists.tracks[i]
        uri_list = [track['track_uri'] for track in playlist]
        
        playlist = songs[[uri in uri_list for uri in songs_df['uri']]]
        
        # Predict the cluster
        
        input_songs_membership = fuzz.cluster.cmeans_predict(playlist.T, cntr, 2, error=0.000005, maxiter=50000)[0]
        
        all_songs_membership_array = []
        for song_membership in all_songs_membership.T:
            all_sorted_indices = np.argsort(song_membership)[::-1]
            all_songs_membership_array.append(all_sorted_indices)

        # Suggest songs from the cluster
        input_songs_membership_sum = np.sum(input_songs_membership.T, axis=0)
        input_songs_membership_sorted_indices = np.argsort(input_songs_membership_sum)[::-1]

        target_array = input_songs_membership_sorted_indices[0:refinement]

        matching_indices = []

        # Iterating over the array list
        for index, arr in enumerate(all_songs_membership_array):
            # Checking if the first two entries match

            if np.array_equal(arr[:refinement], target_array):
                matching_indices.append(index)
        
        recs.append(songs_df[[i in matching_indices for i in range(len(songs_df))]].sample(n_suggestions).to_dict(orient='records'))
    
    recs_s = pd.Series(recs)

    return evaluate(recs_s, val_songs)