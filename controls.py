"""
This file comprises of functions related to controlling playback.
"""

def find_song(spObject, query, count=10):
    """
    Yes, this technically isn't directly related to controlling playback, but I think it makes the most sense to categorize here since it's really nice to integrate with the add_to_queue
    function.

    This is a function that finds the uri of the most related SONGs for a given query.

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope "user-read-private"

    query: str
        String to query the spotify api...things like artist/song/market can be specified using tags 
        (https://developer.spotify.com/documentation/web-api/reference/#endpoint-search for more info)

    count: int (opt.)
        Integer specifying how many results to return; defaults to 10

    Returns
    -------

    results: list
        List containing dictionaries for each result. Dictionaries have the format {
            "artist": artist (str),
            "album": album (str),
            "name": name (str),
            "uri": uri (str)
        }
    """

    #ensure that the count given is below the limit of 50 and not below 1.
    if count < 1:
        count = 1
    elif count > 50:
        count = 50

    data = spObject.search(query, limit=count, type='track')
    results = []
    
    for result in data["tracks"]["items"]:
        results.append({
            "artist": result["artists"][0]["name"],
            "album":result["album"]["name"],
            "name": result["name"],
            "uri": result["uri"]
        })

    return results

def add_song_to_queue(spObject, songData):
    """
    Function that adds a song to the user's queue based on the song's data (uri, id, url)

    Parameters
    ----------
    
    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    songData: str
        Desired song's uri, id, or url

    Returns
    -------

    None
    """

    spObject.add_to_queue(songData)

def skip_next(spObject):
    """
    Skips to the next song in the user's queue.

    Parameters
    ----------
    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    Returns
    -------
    
    None
    """
    
    spObject.next_track()

def skip_previous(spObject):
    """
    Skips to the previous song in the user's queue.

    Parameters
    ----------
    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    Returns
    -------
    
    None
    """
    
    spObject.previous_track()

def play_pause(spObject, playback_state=None):
    """
    Pauses playback if something is currently playing, stops playback if nothing is. 

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    playback_state: bool (opt.)
        Desired playback state, if any; True if playing, False otherwise
        If no playback_state given, will automatically toggle playback

    Returns
    -------
    
    newPlaybackState: bool
        Updated playback state; see above
    """

    from playback import check_playing

    if playback_state != None:
        if playback_state: #explicitly asks to pause playback
            spObject.pause_playback()
            newPlaybackState = False
        else: #explicitly asks to play playback
            spObject.start_playback()
            newPlaybackState = True
        
    else: #no explicit playback mode set, run auto-toggling system
        if check_playing():
            spObject.pause_playback()
            newPlaybackState = False
        else:
            spObject.start_playback()
            newPlaybackState = True
        
    return newPlaybackState

def get_devices(spObject):
    """
    Gets a list of the user's currently available devices. Like find_song(), this isn't directly related to playback, but is nice to include with switch_to_device().

    Parameters
    ----------
    
    spObject: spotipy API object
        Spotipy object with scope 'user-read-playback-state'

    Returns
    -------
    
    results: list
        List containing dictionaries of results. Each dictionary has the format {
            "name": name,
            "type": type (computer, smartphone, etc.),
            "id": id
        }

    """
    
    data = spObject.devices()
    results = []
    for result in data["devices"]:
        results.append({
            "name": result["name"],
            "type": result["type"],
            "id": result["id"]
        })

    return results

def switch_to_device(spObject, device_id):
    """
    Switches playback to the device specified and starts it.

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    Returns
    -------

    None
    """
    
    spObject.transfer_playback(device_id, force_play=True)

def get_playlists(spObject, username, display_username, count=20):
    """
    Gets up to 50 of the user's playlists. Like get_devices() and find_song(), will be nice to use with switch_to_playlist().

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'playlist-read-private'
    
    username: str
        Username of the current spotify user; to make owner names prettier when the owner's playlists are returned

    display_username: str
        Display username of the current spotify user; see above

    count: int (opt.)
        Integer from 1 to 50; denotes maximum number of results. Default 20

    Returns
    -------

    results: list
        List containing dictionaries of each result. Dictionaries have the format {
            "name": name,
            "owner": owner,
            "id": id
        }

    """

    #check to make sure count isn't below 1 or above 50
    if count < 1:
        count = 1
    elif count > 50:
        count = 50

    data = spObject.current_user_playlists(limit = count)
    results = []

    for result in data["items"]:
        temp_dict = {
            "name": result["name"],
            "id": result["uri"],
            "owner": "temp"
        }

        if result["owner"]["id"] == username:
            temp_dict["owner"] = display_username
        else:
            temp_dict["owner"] == username
        
        results.append(temp_dict)
    
    return results

def switch_to_playlist(spObject, playlist_id):
    """
    Switches playback to the given playlist.

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    playlist_id: str
        String containing the id of the playlist to switch playback to

    Returns
    -------

    None
    """

    spObject.start_playback(context_uri=playlist_id)

def change_repeat(spObject, current_repeat_type):
    """
    Shifts the repeat state of the playback 1 forward.

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'
    
    current_repeat_type: str
        Current repeat type; can be "song", "playlist", or "none"; this will be cycled 1 forward

    Returns
    -------

    new_repeat_type: str
        New repeat type; see above
    """

    if current_repeat_type == "song":
        new_repeat_type = "playlist"
    elif current_repeat_type == "playlist":
        new_repeat_type = "none"
    else:
        current_repeat_type = "song"

    spObject.repeat(new_repeat_type)
    
    return new_repeat_type

def set_repeat(spObject, repeat_state):

    """
    Uses change_repeat() to set repeat state to a certain value.

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'
    
    repeat_type: str
        Desired repeat state    

    Returns
    -------

    new_repeat_type: str
        New repeat type; see above
    """

    if repeat_state == "song":
        new_repeat_type = change_repeat(spObject, "none")
    elif repeat_state == "playlist":
        new_repeat_type = change_repeat(spObject, "song")
    else:
        new_repeat_type = change_repeat(spObject, "playlist")
    
    return new_repeat_type

def set_shuffle(spObject, shuffle_state):
    """
    Toggles shuffle mode.

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    shuffle_state: bool
        Desired shuffle state; True if shuffle, False if not shuffle

    Returns
    -------

    new_shuffle_state: bool
        New shuffle state; see above
    """

    spObject.shuffle(shuffle_state)
    
    new_shuffle_state = shuffle_state
    return new_shuffle_state

def set_volume(spObject, volume_level):
    """
    Sets playback volume to the specified level.

    Parameters
    ----------

    spObject: spotipy API object
        Spotipy object with scope 'user-modify-playback-state'

    volume_level: int
        Value between 0 and 100 representing the desired volume level

    Returns
    -------

    None
    """

    spObject.volume(volume_level)
