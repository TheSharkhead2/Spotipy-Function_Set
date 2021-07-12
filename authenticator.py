"""
This file adds a class which can be used to automatically re-authenticate the spotipy API
whenever the key expires. This class is intended to be inherited by specific modules

"""

#importing external modules 
import spotipy
import spotipy.util as util    

class ReauthenticationDecorator:
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
                args[0].refresh_token_function()
                return func(*args, **kwargs)

        return wrapper
        

class Authenticator:

    def __init__(self, CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope):
        self._CLIENT_ID = CLIENT_ID
        self._CLIENT_SECRET = CLIENT_SECRET
        self._USERNAME = SPOTIFY_USERNAME
        self.redirect_uri = redirect_uri
        self.scope = scope

        self._create_user_object()
    
    def _create_user_object(self):
        """
        Set up access token and spotipyObject.
        
        """

        token = util.prompt_for_user_token(self._USERNAME, self.scope, self._CLIENT_ID, self._CLIENT_SECRET, self.redirect_uri)
        self.spotipyObject =  spotipy.Spotify(auth=token)

    