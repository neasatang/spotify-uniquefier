# spotify-uniquefier
Creates a Spotify playlist that finds the unique songs between two playlists and puts them into a new playlist while updating and checking for duplicates and hence removing songs that are no longer unique in the playlist.

Firstly, you must have the Spotipy library imported and Flask installed. Just type `pip install spotipy` into the terminal. After that has finished installed, type `pip install Flask` to get Flask installed.

Then, `git clone` the repo into whereever and `cd` into it.

Next, in the Developer section of spotify, create an App and get your client credientials from there.
Ensure that you are in the repo and in the terminal you go: `export SPOTIPY_CLIENT_ID='insert_client_id'`, 
`export SPOTIPY_CLIENT_SECRET='insert_client_secret'` and  `export SPOTIPY_REDIRECT_URI='insert_redirect_uri'`. Ensure that the redirect uri matches the redirect uri from your Spotify App page.

Type `export FLASK_APP=uniqueSongs.py` to create the playlist that identifies the unique songs. Then to update, simply change the file name to `updatePlaylist.py` to update the playlist without having to create a new one each time.

Type `flask run` and then open `127.0.0.1:5000/` in your browser. Check Spotify and voilà.



