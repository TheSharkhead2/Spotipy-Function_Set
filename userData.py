"""
This file contains functions (wrapped in class) relating to gathering data on "current user"

"""

#importing libraries 
from SpotipyFunction_Set.authenticator import Authenticator, ReauthenticationDecorator

class UserData(Authenticator):
    """
    This class is a conglomerate of functions relating to user data querries in the Spotipy library 
    (Spotify API python port). This class inherits from the Authenticator class and can therefore 
    reauthenticate the API access token when need be. Each function that needs this functionality should 
    have the decorator: @ReauthenticationDecorator.reauthorization_check. As this is a child of the 
    Authenticator class, it also requires the same input parameters when initializing the class.

    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope):

        super().__init__(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope)
    
    @ReauthenticationDecorator.reauthorization_check
    def get_top_artists(self, limit=20, offset=0, timeRange='m'):
        """
        Returns the top artists of current user. Requires scope: "user-top-read"

        Parameters
        ----------

        limit: int, optional
            How many artists should be returned. Default = 20. 
        offset: int, optional 
            Offset for top artists, how far forward from top (an offset of 10 would return artists starting at the 10th highest).
        timeRange: str, optional 
            Over what time frame top artists are picked from. Either: s (short term), m (medium term), l (long term)

        """

        timeRangeDef = {'s' : 'short_term', 'm' : 'medium_term', 'l' : 'long_term'} #dict to translate single letter inputs into strings used by Spotipy 

        topArtistsRaw = self.spotipyObject.current_user_top_artists(limit=limit, offset=offset, time_range=timeRangeDef[timeRange]) #grab all the random stuff spotify spits at you here

        topArtistsRaw = topArtistsRaw['items'] #take out only list of artists

        topArtists = {} #empty dictionary to reformat into
        topArtistsName = [] #empty list to only return artist names (easier to use in some instances)
        usefulKeys = ['followers', 'genres', 'name', 'popularity'] #list of all datapoints on each artist we want to keep... All dict keys here: ['external_urls', 'followers', 'genres', 'href', 'id', 'images', 'name', 'popularity', 'type', 'uri']
        for artist in topArtistsRaw:
            artistData = {} #empty dict to store only useful info on artists
            for key in usefulKeys: #grab only the artist data we actually want
                artistData[key] = artist[key]

            topArtists[artist['id']] = artistData #add data in reference to artist id
            topArtistsName.append(artist['name']) #add just artist name to ranked list in order to more easily see top artists at a glance

        return (topArtistsName, topArtists)