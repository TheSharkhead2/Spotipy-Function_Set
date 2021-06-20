""" 
This file comprises functions that have to do with data on currently playing music. 
"""

def basic_song_info(spObject):
    """ 
    Return basic data for currently playing song. This is intended for use with 
    programs displaying the currently playing song. 

    Parameters 
    ----------
    spObject: Spotipy API Object 
        Spotipy object with scope of: 'user-read-currently playing'

    Returns
    -------
    songID: str 
        The Spotify song id as a string
    artist: str 
        The artist name as a string 
    songName: str 
        The name of the song as a string 
    albumName: str 
        The name of the album as a string 
    albumCoverURL: str 
        URL for the cover image of the song album 

    """

    trackInfo = spObject.current_user_playing_track() #get track info for current track
    #future addition: error handling for errors with collecting data... ie: detect if user object needs re-authentication/if user not playing music 

    artist = trackInfo["item"]["artists"][0]["name"] #get first artist listed 
    songName = trackInfo["item"]["name"] #get song name
    albumName = trackInfo["item"]["album"]["name"] #get album name
    albumCoverURL = trackInfo['item']['album']['images'][0]['url'] #get album image url
    songID = trackInfo['item']['id']

    return ((artist, songName, albumName, albumCoverURL, songID))
