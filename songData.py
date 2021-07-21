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
    def artist_top_tracks(self, artistID, country='US') -> list:
        """
        Get top 10 tracks for an artist by country. 

        Parameters
        ----------

        artistID: str
            The artist ID, URI, or URL

        country: str 
            Country code to which response should be limited to
        
        Returns 
        -------

        topTracks: list 
            List of top tracks (in order). Each track is a dict with basic information on track. 

        """

        tracksRaw = self.spotipyObject.artist_top_tracks(artist_id=artistID, country=country) #get everything spotipy returns here 

        tracksRaw = tracksRaw['tracks'] #just remove outer dict which does nothing

        topTracks = [] #empty list to reformat into 
        for track in tracksRaw:
            trackFormatted = {'id': track['id'], 'name' : track['name'], 'popularity' : track['popularity']} #dict to reformat track into. Also carry over id, name, and popularity (all which need no extra formatting)

            trackFormatted['album'] = {'id' : track['album']['id'], 'name' : track['album']['name']} #for album, keep only id and name of album 

            artistsFormatted = [] #empty list to reformat artists into 
            for artist in track['artists']:
                artistsFormatted.append({'name' : artist['name'], 'id' : artist['id']}) #for each artist, keep only name and id 
            
            trackFormatted['artists'] = artistsFormatted #add formatted artist list to formatted track dict 

            topTracks.append(trackFormatted) #add to "master" list 


        return topTracks

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
    
    @ReauthenticationDecorator.reauthorization_check
    def categories(self, country=None, locale=None, limit=20, offset=0) -> list:
        """
        This simply returns spotipy.categories() (with very, very minimal formatting) as of now. As I don't understand entirely what these are, this is about
        as much information as I can provide. This is mostly here for completeness. 

        Parameters
        ----------

        country: str, optional 
            Country code for location of categories 

        locale: str, optional 
            Desired language for categories 

        limit: int, optional 
            The maximum number of items to return. Default 20, min 1, max 50 

        offset: int, optional 
            The index of the first item to return. Default 0. 
        
        Returns
        -------

        categories: list
            List of all categories from request

        """

        categoriesRaw = self.spotipyObject.categories(country=country, locale=locale, limit=limit, offset=offset)

        return categoriesRaw['categories']['items']
    
    @ReauthenticationDecorator.reauthorization_check
    def category(self, categoryID, country=None, locale=None) -> dict:
        """
        Returns information on Spotify category. As with the categories() function, I don't fully understand these or their purpose
        so I cannot add much more information. This is mostly here for completeness. 

        Parameters 
        ----------

        categoryID: str
            ID of category  
        
        country: str, optional 
            Country code for country with category 

        locale: str, optional 
            Desired language of category. 
        
        Returns
        -------

        category: dict
            Dictionary with information on category. 

        """

        categoryRaw = self.spotipyObject.category(category_id=categoryID, country=country, locale=locale)

        return categoryRaw

    @ReauthenticationDecorator.reauthorization_check
    def category_playlists(self, categoryID=None, country=None, limit=20, offset=0) -> list:
        """
        Get a list of playlists for a specific Spotify category. Does limited formatted (through removing
        unnecessary information) to spotipy.category_playlists(). 

        Parameters
        ----------

        categoryID: str, optional 
            ID of Spotify category. 

        country: str, optional 
            Country code to specify country 

        limit: int, optional 
            The maximum number of items to return. Default 20, min 1, max 50. 

        offset: int, optional 
            The index of the first item to return. Default 0. 
        
        Returns
        -------

        playlists: list 
            List of playlists in category. 

        """

        playlistsRaw = self.spotipyObject.category_playlists(category_id=categoryID, country=country, limit=limit, offset=offset) #get all that is returned by spotify API

        playlistsRaw = playlistsRaw['playlists']['items'] #remove unecessary dicts 

        playlists = [] #empty list to reformat into 
        for playlist in playlistsRaw:
            #grab all useful information from each playlist and append to new, empty list
            playlists.append({
                'name' : playlist['name'],
                'id' : playlist['id'],
                'description' : playlist['description'],
                'owner' : {'display_name' : playlist['owner']['display_name'], 'id' : playlist['owner']['id']},
                'total_tracks' : playlist['tracks']['total']
            })

        return playlists
    
    @ReauthenticationDecorator.reauthorization_check
    def playlist(self, playlistID, market=None, detailed=False):
        """
        Get information on specified playlist. Will apply some formatting (removing unnecessary information) if detailed=False (or 
        default value). Ignoring inputs of additional_types and fields from Spotify API as they seem useless for the application
        of this library or are redundant with the formatting, fields.

        Parameters
        ----------
        
        playlistID: str 
            ID of Spotify playlist 

        market: str, optional 
            Country code to specify market. Default: None. 

        detailed: bool, optional
            If True, will return all information provided by Spotify API function, If False, will apply formatting. Default: False. 

        Returns
        -------

        playlist: dict 
            Dictionary with information on playlist. Note: tracks key does not list ALL tracks. Use playlist_items() function for 
            all tracks. 
        
        """

        rawPlaylist = self.spotipyObject.playlist(playlist_id=playlistID, market=market) #get all information that you would from Spotify API 

        if detailed: #if detailed is True, return everything Spotify API does
            return rawPlaylist

        usefulKeys = ['collaborative', 'description', 'id', 'name', 'public'] #set of useful keys from all dict keys: ['collaborative', 'description', 'external_urls', 'followers', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri']
        returnPlaylist = {} #empty dict to reformat into 

        #take only keys labeled as "useful" in above list
        for key in usefulKeys:
            returnPlaylist[key] = rawPlaylist[key]
        
        returnPlaylist['followers'] = rawPlaylist['followers']['total'] #take total followers instead of dict with total and an href (to nothing most of the time?)
        returnPlaylist['owner'] = {'display_name' : rawPlaylist['owner']['display_name'], 'id' : rawPlaylist['owner']['id']} #take only id and name of playlist owner
        returnPlaylist['total_tracks'] = rawPlaylist['tracks']['total'] #put total tracks into different location in dict 

        tracks = [] #empty list to format tracks into 
        for track in rawPlaylist['tracks']['items']:
            #dict to reformat track into. Also take id, name, and added_at, all needing no extra formatting.
            trackFormatted = {
                'id' : track['track']['id'],
                'name' : track['track']['name'],
                'added_at' : track['added_at']
            } 

            trackFormatted['added_by'] = track['added_by']['id'] #added_by key is just the id of the user who added the song

            artists = [] #empty list to format artists into 
            for artist in track['track']['artists']:
                #take only id and name of each artist 
                artists.append({
                    'name' : artist['name'],
                    'id' : artist['id']
                })
            trackFormatted['artists'] = artists #add to formatted track dict 

            trackFormatted['album'] = {'id' : track['track']['album']['id'], 'name' : track['track']['album']['name']} #take only id and name of album

            tracks.append(trackFormatted) #added formatted track to list of formatted tracks
 
        returnPlaylist['tracks'] = tracks #add formatted tracks list to returnPlaylist

        return returnPlaylist
