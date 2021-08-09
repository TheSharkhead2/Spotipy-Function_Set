# Spotipy Function Set (*Name WIP*) 

[Spotipy](https://github.com/plamere/spotipy) is a Python library that allows for easier use of the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) in Python. This project intends to work through a few of the issues we have found when using Spotipy for our personal projects. Fundementally, all this project is doing is reformatting what Spotipy returns or providing some additional logic to allow for more functionality. 

## Use 

All the functions in this project can be accessed through one class, to import this class into your project simply import: 
```
from SpotipyFunction_Set import Spotipy2
```
We have split up some of the functions within Spotipy into seperate categories: 
```
Spotipy2.Controls
Spotipy2.Playback
Spotipy2.UserData
Spotipy2.SongData
```
These are very loose categories that have functions related to: controlling playback (Controls); information on currently playing track (Playback); information on the current user (UserData); and general information on tracks, albums, artists, etc (SongData). Most of the function names are the same as the functions in the Spotipy library with some differences. 

## Questions

### Why still use Spotipy? 

Currently, simplicity. Yes, more could be done if we would fork Spotipy or write our own code to access the Soptify Web API; however, by just building ontop of Spotipy, we can get this library up and running sooner. 

In the future, if we finish up this library, we will probably consider working on our own version of Spotipy (either by forking or building from scratch); however, for now will we continue to build up from Spotipy. 

### Why is this needed?

When we were working with Spotipy before we started work on this project, we had a handful of issues that held us back from making significant proggress at times. This included, but is not limited to: 
- Spotipy randomly requiring re-authentication 
- Confusing or messy data being returned that was difficult to sift through 
- Programs required significant error handling as Spotipy would easily error if music wasn't being played or if it encountered other somewhat common occurances 

In another way, many of our issues could be traced to simply not understanding the API well enough. By working on this project, we have also been able to get a better grasp on how it functions such that we can more easily work on new projects in the future. 
