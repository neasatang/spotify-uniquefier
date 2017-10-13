from flask import Flask
app = Flask(__name__)

import spotipy
import spotipy.util as util
import json

username='1162445298'
scope = 'playlist-modify-public	'
temp = 'nualaoch'
new_playlist_id='5mP5SMIuWYmAfF5vX86K4L'

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

        total_amount = int(my_amount + other_amount)
        print(total_amount)

        #set the offset variable
        my_increment_amount = 0
        other_increment_amount = 0
        new_increment_amount = 0

        #global arrays
        global total_id_arr
        total_id_arr = []
        global my_id_arr
        my_id_arr = []
        global other_id_arr
        other_id_arr = []
        global combined_id_arr
        combined_id_arr = []

        #loop to go through all of the songs in the playlist
        for i in range(0,my_amount):
            getMoreTracks(playlist_id, sp, my_increment_amount, username)
            my_increment_amount+=100

        for j in range(0,other_amount):
            getMoreTracks(other_playlist_id, sp, other_increment_amount, temp)
            other_increment_amount+=100

        for k in range (0, total_amount):
            getIdOfCombined(username, sp, new_playlist_id, new_increment_amount)
            new_increment_amount += 100

        print(len(combined_id_arr))

        #gets rid of duplicates in total id array
        storage_arr = total_id_arr[:]
        for index,value in enumerate(total_id_arr):
            if value in total_id_arr[index+1:]:
                storage_arr = list(filter((value).__ne__, storage_arr))

        uniq = storage_arr[:]
        comb = combined_id_arr[:]

        for index, value in enumerate(storage_arr):
            if value in comb:
                uniq = list(filter((value).__ne__, uniq))
                comb = list(filter((value).__ne__, combined_id_arr))

        #goes through array that contains the unique songs, and adds them to new playlist
        unique_song_array = []
        count = 0
        for track in uniq:
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
                track = item['track'].get("id", "")
                total_id_arr.append(track)
            else:
                continue

    #goes through other playlist and adds to array
    elif user==temp:
        for item in playlist['items']:
            if item['track'] is not None:
                track = item['track'].get("id", "")
                total_id_arr.append(track)
            else:
                continue

#Function to get the song ids in the old combined playlist
def getIdOfCombined(username, sp, playlist_id,increment_amount):
    playlist = sp.user_playlist_tracks(username, playlist_id, limit=100, offset=increment_amount)
    for item in playlist['items']:
        if item ['track'] is not None:
            track = item['track'].get("id","")
            combined_id_arr.append(track)
        else:
            continue

if __name__ == '__main__':
    app.run(host = '127.0.0.1')