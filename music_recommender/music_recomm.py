#def main():
#    import read_playlists 
#    print('python main function')

if __name__ == '__main__':
    # main()
    import pandas as pd
    from read_playlists import read_file
    from featurization import get_features, merge_track_features_and_playlist
    from k_means import vectorize_text, kmeans_fit, kmeans_predict, add_prediction
    from recommend_util import recommend_util
    fpath = '/home/ernek/Main/Erdos/song_recommender/playlist_data/sampledata'
    fname = 'mpd.slice.0-999.json'
    music_data = read_file(fpath, fname)
    # print(music_data.head())
    
    N = 50
    song_features = get_features(music_data, N)
    music_df = merge_track_features_and_playlist(music_data, song_features, N)

    print(music_df.head())
    
    #print(music_df.keys())
    fraction = 0.4
    #print(music_df.text[int(len(music_df.text)*fraction):])
    X_train = vectorize_text(music_df.text[int(len(music_df.text)*fraction):])
    
    #print(X_train)
    model = kmeans_fit(X_train, 5, 500, 100)
    prediction = kmeans_predict(model, music_df['text'][3])
    
    print('cluster_prediction: ', prediction)

    add_prediction(music_df, model)

    print(music_df['ClusterPrediction'][:4])

    song_choice = 5
    
    original_song , recommended_songs = recommend_util(music_df, music_df['track_artist_name'][song_choice], music_df['track_track_name'][song_choice], model)
    print(original_song)
    print('\n')
    print(recommended_songs)    
    