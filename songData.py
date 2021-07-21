"""
This file contains a class that has functions for more information on songs, artists, albums, etc. 

"""

#importing libraries 
from .authenticator import Authenticator, ReauthenticationDecorator

class SongData(Authenticator):
    """
    This class is a conglomerate of functions relating to song/artist/album/other data querries in the 
    Spotipy library (Spotify API python port). This class inherits from the Authenticator class and can 
    therefore reauthenticate the API access token when need be. Each function that needs this 
    functionality should have the decorator: @ReauthenticationDecorator.reauthorization_check. As this 
    is a child of the Authenticator class, it also requires the same input parameters when initializing 
    the class.

    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope):

        super().__init__(CLIENT_ID, CLIENT_SECRET, SPOTIFY_USERNAME, redirect_uri, scope)

    @ReauthenticationDecorator.reauthorization_check
    def related_artists(self, artistID) -> list:
        """
        This function simply returns spotipy.artist_related_artists() with minimal formatting. Thie means
        it returns a list of similar artists to a specified artist id. 

        Parameters
        ----------

        artistID: str
            Spotify artist ID, URI, or URL

        Returns
        -------

        relatedArtists: list
            List of related artists to specified artist. Each entry is a dict containing the name and id of
            the artist.

        """

        relatedArtistsRaw = self.spotipyObject.artist_related_artists(artist_id=artistID) #get all the raw imformation from spotipy function
        relatedArtistsRaw = relatedArtistsRaw['artists'] #only take artists (returns list of artists inside dict with nothing else)

        relatedArtists = [] #new empty list to put new, formatted artists into 
        for artist in relatedArtistsRaw:
            relatedArtists.append({'name' : artist['name'], 'id' : artist['id']}) #take only name and id

        return relatedArtists

    @ReauthenticationDecorator.reauthorization_check
    def artist(self, artists) -> list:
        """
        This function combines spotipy.artist and spotipy.artists where you can input either a single artist id
        or a list of artist ids to get more information on the artist(s). 

        Parameters
        ----------

        artists: str or list 
            If string, must be 1 artist ID, URI, or URL. If list, must be list of strings that are artist IDs, 
            URIs, or URLs. 

        Returns
        -------

        artistsData: list
            List of all artist information for all requested artists. (Still list if only one artist queried)

        """

        if type(artists) is list:
            return self.spotipyObject.artists(artists)
        else:
            return [self.spotipyObject.artist(artists)]

    @ReauthenticationDecorator.reauthorization_check
    def album(self, albums, detailed=False) -> list:
        """
        This function returns more information on an album (spotipy.album()). Can take either single id as a
        string or many as a list.

        Parameters
        ----------

        albums: str or list 
            If string, must be 1 album ID, URI, or URL. If list, must be list of strings that are album IDs, 
            URIs, or URLs.
        
        detailed: bool, optional 
            If False, will remove mostly useless information provided by Spotify API. If True, nothing will be
            removed. 

        Returns
        -------

        albumData: list 
            List of all album data requested. 

        """

        #if list provided simply pass input into albums(), otherwise put into list and then pass into albums()
        if type(albums) is list:
            rawAlbumData = self.spotipyObject.albums(albums)
        else:
            rawAlbumData = self.spotipyObject.albums([albums])
        
        rawAlbumData = rawAlbumData['albums'] #spotipy returns a dict with one key, albums. This uneeded complexity.
        
        #if detailed is True, return all of what Spotify returns 
        if detailed:
            return rawAlbumData

        albumData = [] #empty list to put reformatted album data into 
        usefulKeys = ['album_type', 'genres', 'id', 'images', 'label', 'name', 'popularity', 'release_date', 'total_tracks'] #only useful information from: ['album_type', 'artists', 'available_markets', 'copyrights', 'external_ids', 'external_urls', 'genres', 'href', 'id', 'images', 'label', 'name', 'popularity', 'release_date', 'release_date_precision', 'total_tracks', 'tracks', 'type', 'uri']
        for album in rawAlbumData:
            reformattedAlbum = {} #empty dict to reformat into 
            for key in usefulKeys: #take only "useful" keys
                reformattedAlbum[key] = album[key]
            
            albumArtists = [] #empty list to put only necessary artist information into 
            for artist in album['artists']:
                albumArtists.append({'id' : artist['id'], 'name' : artist['name']}) #take only artist id and name 

            reformattedAlbum['artists'] = albumArtists #add reformatted artists to reformattedAlbum dict 

            albumTracks = [] #empty list to reformat album tracks into
            for track in album['tracks']['items']:
                albumTracks.append(track['id']) #take only the track id as more information on each track can be requested through other means 
            
            reformattedAlbum['tracks'] = albumTracks #add reformatted tracks to reformatted album dict
            
            albumData.append(reformattedAlbum) #add reformatted dict back to albumData 
        
        return albumData

    @ReauthenticationDecorator.reauthorization_check
    def audio_features(self, tracks, stripID=True) -> list:
        """
        This function is an implementation spotipy.audio_features(). Some of the information returned for each song is 
        removed (from the original spotipy result) meaning each ID provided, returns the information: 
        ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

        This is functionally similar to Playback.get_song_attributes(), however any song ID can be provided (instead of
        only the currently playing song) and any number of IDs can be provided (max 100, so technically not any).  

        Parameters 
        ----------

        tracks: list 
            Any length list which contains Spotify song IDs. 

        stripID: bool, optional 
            If True, default, song ID will be removed from coorisponding dictionary. If False, ID will be kept. 

        Returns
        -------

        audioFeatures: list 
            List of dictionaries that each contain information on each song ID provided.

        """

        audioFeaturesRaw = self.spotipyObject.audio_features(tracks=tracks)

        audioFeatures = [] #empty list to reformat data into
        usefulKeys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature'] #Only look at actual audio features and not other stuff this returns (['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature'])
        for song in audioFeaturesRaw:
            songFeatures = {} #empty dict to put all useful features into 
            for key in usefulKeys:
                songFeatures[key] = song[key]
            
            if not stripID:
                songFeatures['id'] = song['id']

            audioFeatures.append(songFeatures)

        return audioFeatures
    
    @ReauthenticationDecorator.reauthorization_check
    def audio_analysis(self, track) -> dict:
        """
        Currently just returns spotipy.audio_analysis() (I don't have sufficient enough understanding of what this is returning
        to do any formatting)

        Parameters
        ----------

        track: str 
            Spotify track id     

        Returns
        -------

        audioAnalysis: dict 
            A dictionary of information on the track. Has the keys: ['meta', 'track', 'bars', 'beats', 'sections', 'segments', 'tatums']

        Citations
        ---------

        Information on audio analysis: https://www.slideshare.net/MarkKoh9/audio-analysis-with-spotifys-web-api

        """

        audioAnalysisRaw = self.spotipyObject.audio_analysis(track)

        return audioAnalysisRaw