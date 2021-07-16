"""
This file contains functions (wrapped in class) relating to gathering data on "current user"

"""

#importing libraries 
from .authenticator import Authenticator, ReauthenticationDecorator

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

        Returns
        -------

        topArtistsTuple: tuple
            Tuple containing list of top artists in order with names and a list containing more info on each artist (each entry in 
            this list contains dict with more info). In format: (topArtistsName, topArtists)

        """

        timeRangeDef = {'s' : 'short_term', 'm' : 'medium_term', 'l' : 'long_term'} #dict to translate single letter inputs into strings used by Spotipy 

        topArtistsRaw = self.spotipyObject.current_user_top_artists(limit=limit, offset=offset, time_range=timeRangeDef[timeRange]) #grab all the random stuff spotify spits at you here

        topArtistsRaw = topArtistsRaw['items'] #take out only list of artists

        topArtists = [] #empty list to reformat into
        topArtistsName = [] #empty list to only return artist names (easier to use in some instances)
        usefulKeys = ['followers', 'genres', 'name', 'popularity', 'id'] #list of all datapoints on each artist we want to keep... All dict keys here: ['external_urls', 'followers', 'genres', 'href', 'id', 'images', 'name', 'popularity', 'type', 'uri']
        for artist in topArtistsRaw:
            artistData = {} #empty dict to store only useful info on artists
            for key in usefulKeys: #grab only the artist data we actually want
                artistData[key] = artist[key]

            topArtists.append(artistData) #add data back to list
            topArtistsName.append(artist['name']) #add just artist name to ranked list in order to more easily see top artists at a glance

        return (topArtistsName, topArtists)

    @ReauthenticationDecorator.reauthorization_check
    def get_top_tracks(self, limit=20, offset=0, timeRange='m'):
        """
        Returns the top tracks of current user. Requires scope: "user-top-read"
        
        Parameters
        ----------

        limit: int, optional
            How many artists should be returned. Default = 20. 
        offset: int, optional 
            Offset for top artists, how far forward from top (an offset of 10 would return artists starting at the 10th highest).
        timeRange: str, optional 
            Over what time frame top artists are picked from. Either: s (short term), m (medium term), l (long term)
        
        Returns
        -------

        topTracksTuple: tuple
            Tuple containing, in first index, list of only the names of the user's top tracks and, in second index, list of dictionaries containing this information on each song: ['album', 'artists', 'id', 'name', 'popularity'] 

        """

        timeRangeDef = {'s' : 'short_term', 'm' : 'medium_term', 'l' : 'long_term'} #dict to translate single letter inputs into strings used by Spotipy 

        topTracksRaw = self.spotipyObject.current_user_top_tracks(limit=limit, offset=offset, time_range=timeRangeDef[timeRange])

        topTracksRaw = topTracksRaw['items'] #take only list of tracks

        topTracks = [] #empty list to reformat data into 
        topTracksName = [] #empty list to only include track names in 
        usefulKeys = ['album', 'artists', 'id', 'name', 'popularity'] #list of all keys that will be returned with this function. Full list of keys from API is: ['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri']
        for track in topTracksRaw:
            trackData = {} #empty dict to put all relevant track data into
            for key in usefulKeys: #grab only wanted data
                if key == 'album': #if you just use 'album' entry, you get all information on album. For simplicity, only return name of album
                    trackData[key] = track[key]['name']
                elif key == 'artists': #artist also gives more information than necessary... Take out only artist's names
                    artistsList = [] #empty list to keep track of all artist names
                    for artist in track[key]:
                        artistsList.append(artist['name']) #take out only artist name 
                    trackData[key] = artistsList
                else:
                    trackData[key] = track[key]
                
            
            topTracks.append(trackData) #put all useful data into list 
            topTracksName.append(track['name']) #append only name of track to seperate list

        return (topTracksName, topTracks)

    @ReauthenticationDecorator.reauthorization_check
    def recommendation_genre_seeds(self):
        """
        Simply returns spotipy.recommendation_genre_seeds() --> 

        Get a list of genres available for the recommendations function

        Returns
        -------

        genres: list 
            A list of all genres that can be used as seed inputs for get_recommendations()

        """

        return self.spotipyObject.recommendation_genre_seeds()['genres']

    @ReauthenticationDecorator.reauthorization_check
    def get_recommendations(self, seedArtists=None, seedGenres=None, seedTracks=None, limit=20, country=None, **kwargs):
        """
        Returns a certain number of song recommendations based on different seeds. 

        Parameters
        ----------

        seedArtists: list, optional 
            A list of artists IDs, URIs, or URLs 

        seedTracks: list, optional 
            A list of track IDs, URIs, or URLs 

        seedGenres: list, optional 
            A list of genre names. Available genres: ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
        
        min/max/target_<attribute>: any, optional
            attributes that allow for more specificity as to which songs are being requested. More information: https://developer.spotify.com/console/get-recommendations/

        country: str, optional
            An ISO 3166-1 alpha-2 country code. If provided, all results will be playable in this country.

        limit: int, optional
            The maximum number of items to return. Default: 20, min: 1, max: 100. 

        Returns
        -------

        recommendations: list 
            List of all track recommendations including album, artists, track id, and track name

        """

        #get just the raw recommendations from spotipy without any formatting
        recommendationsRaw = self.spotipyObject.recommendations(seed_artists=seedArtists, seed_genres=seedGenres, seed_tracks=seedTracks, limit=limit, country=country, kwargs=kwargs)
        recommendationsRaw = recommendationsRaw['tracks'] #take just the tracks from the recommendations return and not the information on seeds

        recommendations = [] #empty list to reformat data into 
        usefulKeys = ['album', 'artists', 'id', 'name'] #list of all keys that will be returned with this function. Full list of keys from API is: ['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri']
        for recommendation in recommendationsRaw:
            trackData = {} #empty dict to put all relevant track data into
            for key in usefulKeys: #grab only wanted data
                if key == 'album': #if you just use 'album' entry, you get all information on album. For simplicity, only return name of album
                    trackData[key] = recommendation[key]['name']
                elif key == 'artists': #artist also gives more information than necessary... Take out only artist's names
                    artistsList = [] #empty list to keep track of all artist names
                    for artist in recommendation[key]:
                        artistsList.append(artist['name']) #take out only artist name 
                    trackData[key] = artistsList
                else:
                    trackData[key] = recommendation[key]
                
            
            recommendations.append(trackData) #put all useful data into list 

        return recommendations