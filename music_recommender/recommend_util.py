import k_means
import pandas as pd

def recommend_util(data, artist_name, song_name, model):
    
    # Predict category of input string category
    chosen_song_df = data.loc[(data['track_artist_name'] == artist_name) & (data['track_track_name'] == song_name)]
    str_input = chosen_song_df.text
        
    prediction_inp = k_means.kmeans_predict(model, str_input)
    prediction_inp = int(prediction_inp)
    
    temp_df = data.loc[data['ClusterPrediction'] == prediction_inp]
    
    Nsongs = len(temp_df.index)
    if Nsongs <= 5:
        new_temp_df = temp_df.sample(Nsongs - 1, random_state = 2)
    else:
        new_temp_df = temp_df.sample(5, random_state=2)
    
    print(new_temp_df)
    
    for indx, recommendation in new_temp_df.iterrows():
        print(indx , recommendation['track_artist_name'], chosen_song_df['track_artist_name'].values[0])
        if (recommendation['track_artist_name'] == chosen_song_df['track_artist_name'].values[0]) and (recommendation['track_track_name'] == chosen_song_df['track_track_name'].values[0]):
           print('recommended same chosen song')
           new_recommendation = temp_df.sample(1, random_state=1)
           new_temp_df.drop(index = indx, inplace = True)
           print(new_temp_df)
           new_temp_df = pd.concat((new_temp_df, new_recommendation), axis=0)
           print(new_temp_df)
           break
        
    return chosen_song_df[['track_artist_name', 'track_track_name']], new_temp_df[['track_artist_name', 'track_track_name']]