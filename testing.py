import pandas as pd
import numpy as np
import json
from math import floor
from copy import deepcopy

root_path = !pwd
root_path = str(root_path[0])
filepath = f"{root_path}/playlist_data/sampledata/"
filename = 'mpd.slice.0-999.json'
fpath_name = f"{filepath}{filename}"
with open(fpath_name) as data_file:    
    data = json.load(data_file)
    
playlists = pd.json_normalize(data['playlists'])

def get_score(pred_songs, true_songs):
    
    true_songs = pd.DataFrame(true_songs)
    pred_songs = pd.DataFrame(pred_songs)
    
    artist_score = pred_songs.artist_name.apply(lambda x: x in true_songs.artist_name.values).sum()
    track_score = pred_songs.track_name.apply(lambda x: x in true_songs.track_name.values).sum()
    
    score = artist_score + track_score

    return score/(2*len(pred_songs))


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
    
    scores = [get_score(suggestions['tracks'][i], val_songs[i]) for i in suggestions.pid]
    
    return sum(scores)/len(suggestions)