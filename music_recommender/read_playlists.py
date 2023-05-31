import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import json
import spotipy
import pickle


def read_file(fpath,*playlist_files):
    """
    Read a json file containing playlist information 
    Args:
    fpath_name -> directory path to where the playlist files are
    playlist_files -> one or multiple file names
    """
    for file in playlist_files:
        filepath = f"{fpath}/{file}"
        print(filepath)
        with open(filepath) as data_file:    
            data = json.load(data_file)  
        for index, playlist in enumerate(data['playlists']):
            num_keys =  len(playlist.keys())
            if index == 0:
                num_key_old = num_keys
                continue
            if num_keys > num_key_old:
                keys = playlist.keys()
            num_key_old = num_keys
        keys = list(keys)
        keys.remove('tracks')
        print(" Playlist keys: ", keys)
        music_df = pd.json_normalize(data['playlists'],  meta = keys, meta_prefix = 'playlist_', errors='ignore', record_path=['tracks'], record_prefix = 'track_')
        return music_df
    