import k_means

def recommend_util(data, artist_name, song_name, model):
    
    # Predict category of input string category
    chosen_song_df = data.loc[(data['track_artist_name'] == artist_name) & (data['track_track_name'] == song_name)]
    str_input = chosen_song_df.text
        
    prediction_inp = k_means.kmeans_predict(model, str_input)
    prediction_inp = int(prediction_inp)
    
    temp_df = data.loc[data['ClusterPrediction'] == prediction_inp]
    new_temp_df = temp_df.sample(2)
    
    return chosen_song_df[['track_artist_name', 'track_track_name']], new_temp_df[['track_artist_name', 'track_track_name']]