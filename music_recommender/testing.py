import pandas as pd
import numpy as np
import json
from math import floor
from copy import deepcopy
import os


root_path = os.getcwd()
filepath = f"{root_path}/playlist_data/sampledata/"
filename = 'mpd.slice.0-999.json'
fpath_name = f"{filepath}{filename}"
with open(fpath_name) as data_file:    
    data = json.load(data_file)
    
playlists = pd.json_normalize(data['playlists'])

def get_score(pred_songs, true_songs):
    
    pred_artists = {track['artist_name'] for track in pred_songs}
    true_artists = {track['artist_name'] for track in true_songs}
    pred_tracks = {track['track_name'] for track in pred_songs}
    true_tracks = {track['track_name'] for track in true_songs}

    artist_score = len(pred_artists.intersection(true_artists))
    track_score = len(pred_tracks.intersection(true_tracks))
    

    return [artist_score/(len(pred_artists)), track_score/(len(pred_tracks))]


def evaluate(suggestions, val_ratio=0.2):
    
    """
    
    Args:
        
        suggestions (DataFrame): Must have two columns 'pid' (playlist id) and 'tracks' (the suggested tracks).
        
        val_ratio (float): Ratio of songs in each playlist to withhold. Must be in between 0 and 1. When modeling the suggestions
            you should use only the first 1-val_ratio part of each playlist.
        
    Return:
    
        float: For each suggested song we get 1/2 each if artist/track is in the withheld tracks. The return is the
            average score per suggestion. Perfect score is 1 while no match at all gives 0.
    
    """
    
    val_songs = playlists.tracks.apply(lambda x: x[max(1,floor(len(x)*(1-val_ratio))):])
    total_score = suggestions
    
    scores = np.array([get_score(suggestions['tracks'][i], val_songs[i]) for i in suggestions.pid])

    result = {'artist_match_rate':np.mean(scores, axis=0)[0], 'track_match_rate':np.mean(scores,axis=0)[1]}
    
    return result



