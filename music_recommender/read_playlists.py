import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import json
import spotipy
import pickle


def get_song_dataframe(path):
    # returns a dataframe of all of the songs in the million playlist data set
    # path - a string containing a path to the folder where the csv files are held.
    #        for example, on my machine, the folder where I ran this script also contained a folder
    #        called "song_data" which had the csv files in it. So I called get_song_dataframe('song_data/')
    #        NOTE - Make sure to include the slash!
    file_name_list = ['song.slice.' + str(i) + '-' + str(i + 49999) + '.csv' for i in range(0,2212292, 50000)] 
    file_name_list = file_name_list + ['song.slice.2250000-2262292.csv']
                        
    df_list = []
    for file_name in file_name_list:
        df_list.append(pd.read_csv(path + file_name))
    
    data = pd.concat(df_list)
    return data

def get_artist_dataframe(path): 
    # returns a dataframe of all of the artists in the million playlist data set
    # The only attributes included are "followers", "name", "uri", "genres", "popularity"
    # WARNING - Some artists have no genres, in this case the value is an empty list
    # path - a string containing a path to the folder where the csv files are held.
    #        for example, on my machine, the folder where I ran this script also contained a folder
    #        called "song_data" which had the csv files in it. So I called get_song_dataframe('song_data/')
    #        NOTE - Make sure to include the slash!
    dfs = [pd.read_csv(path + 'artist.slice.0-99999.csv'), pd.read_csv(path + 'artist.slice.100000-199999.csv'), pd.read_csv(path + 'artist.slice.200000-295859.csv')]
    df = pd.concat(dfs)
    del df['Unnamed: 0.1']
    del df['Unnamed: 0']
    
    return df

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
    
