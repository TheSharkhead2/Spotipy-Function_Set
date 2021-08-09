"""
This file contains a so-called "main class" which allows for the user to 
create only an instance of this class and still call functions from all
other classes (ie, it "holds" instances of all other classes). 

"""

#import classes 
from .controls import Controls
from .playback import Playback
from .songData import SongData
from .userData import UserData

class Spotipy2:
    """
    This class is a compiled version of the various classes within this module. The aim
    of this module overall is to act as a so called "compatibility layer" over the Python
    Spotify API library, Spotipy. Many of the functions within the Spotipy library can
    return "messy" data or could be used slightly differently to get more use from them. 
    This module aims to make changes to what Spotipy would return such that it can be
    more useful in certain circumstances. 

    INIT Parameters
    ---- ----------
    
    CLIENT_ID: str 
        Spotify client id for API 

    CLIENT_SECRET: str 
        Spotify client secret for API 

    SPOTIFY_USERNAME: str 
        Spotify username for user "using" this API/library 

    redirect_uri: str 
        Redirect URI for Spotify API 

    scope: str 
        Scope for using Spotify API 

    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope) -> None:

        #Save variables as class properties, simplifies changing the scope and adding other future functionality
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.SPOTIFY_USERNAME = SPOTIFY_USERNAME
        self.redirect_uri = redirect_uri
        self.scope = scope

        #Define all "subclasses"
        self.Controls = Controls(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, self.scope)
        self.Playback = Playback(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, self.scope)
        self.SongData = SongData(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, self.scope)
        self.UserData = UserData(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, self.scope)

    def change_subclass_scopes(self, new_scope) -> None:

        #redefine all "subclasses" according to the needed new scope
        self.Controls = Controls(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, new_scope)
        self.Playback = Playback(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, new_scope)
        self.SongData = SongData(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, new_scope)
        self.UserData = UserData(self.CLIENT_ID, self.CLIENT_SECRET, self.SPOTIFY_USERNAME, self.redirect_uri, new_scope)