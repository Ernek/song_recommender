#def main():
#    import read_playlists 
#    print('python main function')

if __name__ == '__main__':
    # main()
    import pandas as pd
    from read_playlists import read_file
    from featurization import get_features, merge_track_features_and_playlist
    fpath = '/home/ernek/Main/Erdos/song_recommender/playlist_data/sampledata'
    fname = 'mpd.slice.0-999.json'
    music_data = read_file(fpath, fname)
    # print(music_data.head())
    
    N = 10 
    song_features = get_features(music_data, N)
    music_df = merge_track_features_and_playlist(music_data, song_features, N)

    print(music_df.head())
    
    print(music_df.keys())
    

    