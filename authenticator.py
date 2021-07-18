"""
This file adds a class which can be used to automatically re-authenticate the spotipy API
whenever the key expires. This class is intended to be inherited by specific modules

"""

#importing external modules 
import spotipy
import spotipy.util as util    

class ReauthenticationDecorator:
    """
    THIS IS ONLY A WRAPPER CLASS. DO NOT CREATE AN INSTANCE OF THIS CLASS.

    This class is used to store the decorator necessary to refresh the spotipy
    API token when it expires. This needs to be used only in classes that inherit 
    from the class: Authenticator. 

    """

    @classmethod
    def reauthorization_check(cls, func):
        """
        Should be used as decorator to catch errors when running functions. This 
        is specifically made to deal with periodic "timing out" of the Spotipy 
        object. If an error is caught, this will simply attempt to refresh the 
        token and run the function again. 

        """
        
        def wrapper(*args, **kwargs):
            #if an error occurs when running function, assume spotipy timing out error and refresh token 
            try: 
                return func(*args, **kwargs)
            except:
                print("Spotipy token may be expired... Refreshing token...")
                args[0]._create_user_object()
                return func(*args, **kwargs)

        return wrapper
        

class Authenticator:
    """
    Parent Class
    ------ -----

    This is a class that can be inherited from inorder to allow each library 
    to reauthenticate with spotipy when necessary. Each new library should be 
    a class that inherits from this one. 

    Parameters
    ----------

    CLIENT_ID: str 
        Spotify API client id. 

    CLIENT_SECRET: str
        Spotify API client secret. 

    SPOTIFY_USERNAME: str
        Spotify username for user using program.

    redirect_uri: str 
        Redirect uri for Spotify API calls. 

    scope: str 
        Scope for using Spotify API

    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope):
        self._CLIENT_ID = CLIENT_ID
        self._CLIENT_SECRET = CLIENT_SECRET
        self._USERNAME = SPOTIFY_USERNAME
        self.redirect_uri = redirect_uri
        self.scope = scope

        self._create_user_object()
    
    def _create_user_object(self) -> None:
        """
        Set up access token and spotipyObject.
        
        """

        token = util.prompt_for_user_token(self._USERNAME, self.scope, self._CLIENT_ID, self._CLIENT_SECRET, self.redirect_uri)
        self.spotipyObject =  spotipy.Spotify(auth=token)

    