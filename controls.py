"""
This file comprises of functions related to controlling playback.
"""

#importing libraries
from .authenticator import Authenticator, ReauthenticationDecorator

class Controls(Authenticator):
    """
    This class is a conglomerate of functions relating to controls in the Spotipy library (Spotify API python port).
    This class inherits from the Authenticator class and can therefore reauthenticate the API access token when need 
    be. Each function that needs this functionality should have the decorator: 
    @ReauthenticationDecorator.reauthorization_check. As this is a child of the Authenticator class, it also requires
    the same input parameters when initializing the class.

    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope):

        super().__init__(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope)

    @ReauthenticationDecorator.reauthorization_check
    def check_playing(self) -> bool:
        """
        Return the is_playing boolean to see if spotify is currently playing anything.
        This should be run before other playback functions to prevent indexing errors.
        Needs scope: 'user-read-currently playing'

        Returns
        -------
        isPlaying: bool
            Boolean denoting whether Spotify is currently playing or not

        """

        trackInfo = self.spotipyObject.current_user_playing_track() #get track info for current track
        
        try:
            isPlaying = trackInfo["is_playing"]
        except:
            isPlaying = False

        return isPlaying

    @ReauthenticationDecorator.reauthorization_check
    def playback_settings_info(self) -> "tuple[str, str, dict]": #this doesn't seem fully implemented 
        """
        Gets data about current playback's settings: shuffle state, repeat state, and device id/name/type.

        Returns
        -------

        tuple[shuffle_state, repeat_state, device_info]
            shuffle_state: str
                True if playback is currently shuffling, False otherwise

            repeat_state: str
                "none", "track", or "playlist" depending on current repeat state

            device_info: dict
                dictionary with device info using the format {
                    "id": device id,
                    "name": device name,
                    "type": device type
                }

        """

        data = self.spotipyObject.current_playback()

        shuffle_state = data["shuffle_state"]
        repeate_state = data["repeat_state"]
        device_info = {
            "id": data["device"]["id"],
            "name": data["device"]["name"],
            "type": data["device"]["type"]
        }

        return shuffle_state, repeate_state, device_info

    @ReauthenticationDecorator.reauthorization_check
    def find_song(self, query, count=10) -> list:
        """
        Yes, this technically isn't directly related to controlling playback, but I think it makes the most sense to categorize here since it's really nice to integrate with the add_to_queue
        function.
        This is a function that finds the uri of the most related SONGs for a given query. 
        Needs scope of: "user-read-private"

        Parameters
        ----------

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

        data = self.spotipyObject.search(query, limit=count, type='track')
        results = []
        
        for result in data["tracks"]["items"]:
            results.append({
                "artist": result["artists"][0]["name"],
                "album":result["album"]["name"],
                "name": result["name"],
                "uri": result["uri"]
            })

        return results

    @ReauthenticationDecorator.reauthorization_check
    def add_song_to_queue(self, songData) -> None:
        """
        Function that adds a song to the user's queue based on the song's data (uri, id, url)
        Needs scope: 'user-modify-playback-state'

        songData: str
            Desired song's uri, id, or url

        """

        self.spotipyObject.add_to_queue(songData)

    @ReauthenticationDecorator.reauthorization_check
    def skip_next(self) -> None:
        """
        Skips to the next song in the user's queue.
        Needs scope: 'user-modify-playback-state'

        """
        
        self.spotipyObject.next_track()

    @ReauthenticationDecorator.reauthorization_check
    def skip_previous(self) -> None:
        """
        Skips to the previous song in the user's queue. Needs scope: 'user-modify-playback-state'

        """
        
        self.spotipyObject.previous_track()

    @ReauthenticationDecorator.reauthorization_check
    def play_pause(self, playback_state=None) -> bool:
        """
        Pauses playback if something is currently playing, stops playback if nothing is. Needs scope: 'user-modify-playback-state'

        Parameters
        ----------

        playback_state: bool (opt.)
            Desired playback state, if any; True if playing, False otherwise
            If no playback_state given, will automatically toggle playback

        Returns
        -------
        
        newPlaybackState: bool
            Updated playback state; see above

        """

        if playback_state != None:
            if playback_state: #explicitly asks to pause playback
                self.spotipyObject.pause_playback()
                newPlaybackState = False
            else: #explicitly asks to play playback
                self.spotipyObject.start_playback()
                newPlaybackState = True
            
        else: #no explicit playback mode set, run auto-toggling system
            if self.check_playing():
                self.spotipyObject.pause_playback()
                newPlaybackState = False
            else:
                self.spotipyObject.start_playback()
                newPlaybackState = True
            
        return newPlaybackState

    @ReauthenticationDecorator.reauthorization_check
    def get_devices(self) -> list:
        """
        Gets a list of the user's currently available devices. Like find_song(), this isn't directly related to playback, but is nice to include with switch_to_device().
        Needs scope: 'user-read-playback-state'

        Returns
        -------
        
        results: list
            List containing dictionaries of results. Each dictionary has the format {
                "name": name,
                "type": type (computer, smartphone, etc.),
                "id": id
            }

        """
        
        data = self.spotipyObject.devices()
        results = []
        for result in data["devices"]:
            results.append({
                "name": result["name"],
                "type": result["type"],
                "id": result["id"]
            })

        return results

    @ReauthenticationDecorator.reauthorization_check
    def switch_to_device(self, device_id) -> None:
        """
        Switches playback to the device specified and starts it.
        Needs scope: 'user-modify-playback-state'

        """
        
        self.spotipyObject.transfer_playback(device_id, force_play=True)

    @ReauthenticationDecorator.reauthorization_check
    def get_playlists(self, username, display_username, count=20) -> list:
        """
        Gets up to 50 of the user's playlists. Like get_devices() and find_song(), will be nice to use with switch_to_playlist().
        Needs scope: 'playlist-read-private'

        Parameters
        ----------

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

        data = self.spotipyObject.current_user_playlists(limit = count)
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

    @ReauthenticationDecorator.reauthorization_check
    def switch_to_playlist(self, playlist_id) -> None:
        """
        Switches playback to the given playlist.
        Needs scope: 'user-modify-playback-state'

        Parameters
        ----------

        playlist_id: str
            String containing the id of the playlist to switch playback to

        """

        self.spotipyObject.start_playback(context_uri=playlist_id)

    @ReauthenticationDecorator.reauthorization_check
    def change_repeat(self, repeat_state=None) -> str:

        """
        Sets repeat state to a certain value, or alternatively cycles the repeat state 1 forward.
        Needs scope: 'user-modify-playback-state'

        Parameters
        ----------

        repeat_type: str (opt.)
            Desired repeat state: "none", "song", and "playlist"; if None is given will default to cycling 1 setting forward (e.g. "none" --> "song")     

        Returns
        -------

        new_repeat_type: str
            New repeat type; see above

        """

        if repeat_state != None: #new_repeat_state has been explicitly set
            new_repeat_state = repeat_state
        else: #automatically cycle the repeat state 1 forward
            shuffle_state, repeat_state, device_info = self.playback_settings_info()
            if repeat_state == "song":
                new_repeat_state = "playlist"
            elif repeat_state == "playlist":
                new_repeat_state = "none"
            else:
                new_repeat_state = "song"

        self.spotipyObject.repeat(new_repeat_state)

        return new_repeat_state

    @ReauthenticationDecorator.reauthorization_check
    def change_shuffle(self, shuffle_state=None) -> bool:
        """
        Sets shuffle state to a certain value, or alternatively toggles it.
        Needs scope: 'user-modify-playback-state'

        Parameters
        ----------

        shuffle_state: bool (opt.)
            Desired shuffle state; True if shuffle, False if not shuffle; if None is given will default to toggling between shuffle and non-shufffle modes

        Returns
        -------

        new_shuffle_state: bool
            New shuffle state; see above

        """

        if shuffle_state != None: #new_shuffle_state has been explicitly set
            new_shuffle_state = shuffle_state
        else: #automatically toggle the shuffle state
            shuffle_state, repeat_state, device_info = self.playback_settings_info()
            new_shuffle_state = not shuffle_state
        
        self.spotipyObject.shuffle(new_shuffle_state)

        return new_shuffle_state

    @ReauthenticationDecorator.reauthorization_check
    def set_volume(self, volume_level) -> None:
        """
        Sets playback volume to the specified level.
        Needs scope: 'user-modify-playback-state'

        Parameters
        ----------
        
        volume_level: int
            Value between 0 and 100 representing the desired volume level

        """

        self.spotipyObject.volume(volume_level)
