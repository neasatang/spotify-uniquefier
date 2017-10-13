from flask import Flask
app = Flask(__name__)

import spotipy
import spotipy.util as util
import json

username='1162445298'
scope = 'playlist-modify-public	'
temp = 'nualaoch'

@app.route("/")
def hello():

    #declare variables
    playlist_id=None
    other_playlist_id=None
    my_playlist_song_total=0
    other_playlist_song_total=0

    # get token
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_playlists()

        #playlist is each item
        for playlist in results['items']:
            name_of_playlist = playlist['name']

            if name_of_playlist == 'Good':
                other_playlist_id = playlist['id']
                other_playlist_song_total = playlist['tracks']['total']
                print(name_of_playlist)
                print(other_playlist_id)
                print(other_playlist_song_total)


            if name_of_playlist == 'niceness':
                playlist_id = playlist['id']
                my_playlist_song_total = playlist['tracks']['total']
                print(name_of_playlist)
                print(playlist_id)
                print(my_playlist_song_total)

        #calculates the amount of times the call to the api has to be done to loop through entire playlist
        my_amount = int((my_playlist_song_total/100) + 1)
        print('niceness amount: ' + str(my_amount))

        other_amount = int((other_playlist_song_total/100) + 1)
        print('Good amount: ' + str(other_amount))

        #set the offset variable
        my_increment_amount = 0
        other_increment_amount = 0

        #global arrays
        global total_id_arr
        total_id_arr = []
        global my_id_arr
        my_id_arr = []
        global other_id_arr
        other_id_arr = []

        #loop to go through all of the songs in the playlist
        for i in range(0,my_amount):
            getMoreTracks(playlist_id, sp, my_increment_amount, username)
            my_increment_amount+=100

        for j in range(0,other_amount):
            getMoreTracks(other_playlist_id, sp, other_increment_amount, temp)
            other_increment_amount+=100

        #identifies the unique songs
        uniq = {}
        for i in total_id_arr:
            uniq[i] = True

        for i in my_id_arr:
            if i in other_id_arr and i in total_id_arr:
                uniq.pop(i, None)

            else:
                uniq[i] =True

        #stores the unique songs into a list
        uniq_list = list(uniq.keys())
        print(len(uniq_list))
        #create a new playlist
        result = sp.user_playlist_create(username,"poop",public=True)
        new_playlist_id = result['id']

        #goes through array that contains the unique songs
        unique_song_array = []
        count = 0
        for track in uniq_list:
            count+=1
            unique_song_array.append(track)

            if count == 100:
                results = sp.user_playlist_add_tracks(username, new_playlist_id, unique_song_array)
                unique_song_array = []
                count = 0

        if count > 0:
            results = sp.user_playlist_add_tracks(username, new_playlist_id, unique_song_array)
            unique_song_array = []
            count = 0

        return 'hi'

    else:
        print("Can't get token for", username)

#Function to go through the playlist x times 100 -> total number of songs in playlist
def getMoreTracks(playlist_id, sp, increment_amount, user):
    playlist = sp.user_playlist_tracks(user, playlist_id, limit = 100, offset = increment_amount)

    #goes through self playlist and adds to array
    if user==username:
      #gets the id of each song
        for item in playlist['items']:
            if item['track'] is not None:
                track_id = item['track'].get("id", "")
                total_id_arr.append(track_id)
                my_id_arr.append(track_id)
            else:
                continue

    #goes through other playlist and adds to array
    elif user==temp:
        for item in playlist['items']:
            if item['track'] is not None:
                track_id = item['track'].get("id", "")
                total_id_arr.append(track_id)
                other_id_arr.append(track_id)
            else:
                continue

if __name__ == '__main__':
    app.run(host = '127.0.0.1')