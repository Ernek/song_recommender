#def main():
#    import read_playlists 
#    print('python main function')

if __name__ == '__main__':
    # main()
    import pandas as pd
    from read_playlists import read_file
    fpath = '/home/ernek/Main/Erdos/song_recommender/playlist_data/sampledata'
    fname = 'mpd.slice.0-999.json'
    music_data = read_file(fpath, fname)
    print(music_data.head())


    