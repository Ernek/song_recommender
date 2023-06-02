import json
import matplotlib as plt

def plot_hist_tracks_per_playlist(path):
	"""
	Plots a histogram of the number of tracks in each playlist. 
	path - a string representing the file path to the JSON files from the million playlist data set 
	"""
	file_name_list = [path + 'mpd.slice.' + str(i*1000) + "-" + str(i*1000 + 999) + '.json' for i in range(1000)]
	cut_point = 0    # records thousands digit of the curent playlist
	num_tracks_list = [0]*1000000   # initialize list which holds the number of tracks in each playlist

	for file_name in file_name_list:
		# read JSON file, save output and close
    	data_file = open('data/' + file_name)
    	data = json.load(data_file)
    	data_file.close()
    	# for each playlist in the JSON file, record number of tracks
    	for ndx in range(1000):
        	num_tracks_list[cut_point + ndx] = (data['playlists'][ndx])['num_tracks']
    
   		cut_point = cut_point + 1000


    plt.hist(num_tracks_list, range(0,380,10))
    plt.xlabel(xlabel = 'Number of tracks in playlist')
	plt.show()

def plot_hist_tracks_per_playlist(path):
	"""
	Plots a histogram of the number of artists in each playlist. 
	path - a string representing the file path to the JSON files from the million playlist data set 
	"""
	file_name_list = [path + 'mpd.slice.' + str(i*1000) + "-" + str(i*1000 + 999) + '.json' for i in range(1000)]
	cut_point = 0    # records thousands digit of the curent playlist
	num_artists_list = [0]*1000000   # initialize list which holds the number of artists in each playlist

	for file_name in file_name_list:
		# read JSON file, save output and close
    	data_file = open('data/' + file_name)
    	data = json.load(data_file)
    	data_file.close()
    	# for each playlist in the JSON file, record number of unique artists
    	for ndx in range(1000):
        	artist_set = set()
        	tracks = ((data['playlists'])[ndx])['tracks']
        	for track in tracks:
           		artist_set.add(track['artist_uri'])
        	num_artists_list[cut_point + ndx] = len(artist_set)
    
   		cut_point = cut_point + 1000


    plt.hist(num_artists_list, range(0,240,10))
    plt.xlabel(xlabel = 'Number of artists in playlist')
	plt.show()

