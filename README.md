# OnRepeat+ 🎶
---
## What is OnRepeat+ ?

OnRepeat+ is an application that allows a Spotify User to get 90 recommended songs based oh their curent "On Repeat" playlist and their audio features. The recommended songs can com from either a provided dataSet containing over 10'000 songs (mainly songs in English) or the user can also provide the ID of a playlist they want to get the recommendations from. The process would hoever be slower as the application needs to fetch and process all the data on through the spotify API. If the user wants to, the recommendations can be saved in a csv file.


![image](https://user-images.githubusercontent.com/71267194/205450463-62fd06c5-5a35-43f0-945a-804c3e2a5c4e.png)



# Getting Started 🔧

## Libraries 📚
  + please install these libraires if your python environement doesn't have them yet ! 
  + `pip install tk` `pip install scikit-metrics` `pip install pandas`


## Spotify ID 📝
1) Creating a Spotify account and sign up for a [Spotify developper's account](https://developer.spotify.com/dashboard/)
2) Create a new app and get the ClientID and the ClientSecret ID![ClientID and ClientSecret ID](https://user-images.githubusercontent.com/71267194/205448661-d4c553fa-9fc9-4e39-9433-5c724186cdeb.png)
3) Install Spotify's api `pip install spotipy`
4) Input your IDs on line 11 and 12 of the app code. `spotify_cid = 'spotify_cid'`, `spotify_secret = 'spotify_secret'`
 
 
## Folder data 📁
This folder contains 2 datasets: _ddbSpotify.csv_ which contains the data of 10'000 songs and _onRepeat.csv_ which contains the data of my current songs onRepeat. In this folder will also be created a _reco.csv_ file with the song recommended to the user as well as a _ddbSpotifyInput.csv_ which contains the data of a playlist imput by the user in case they want to get the audio analysis of the whole playlist. _reco.csv_ only contains the name, artist and link of a song while the others also contains the audio features of the song 

Collumns of the 'ddb' datasets:
| id | name | artist | lien | danceability | energy | key | loudness | speechiness | acousticness | instrumentalness | liveness | valence | tempo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|5odlY52u43F5BjByhxg7wg | golden hour | JVKE | https://open.spotify.com/track/5odlY52u43F5BjByhxg7wg | 0.515 | 0.593 | 4 | -4.801 | 0.0322 | 0.653 | 0.162 | 0.25 | 0.153 | 94.467 |


# Launch the project ▶️

+ Just run the program, check the settings you want and you're good 😄

![Image of OnRepeat+ output](https://user-images.githubusercontent.com/71267194/205446977-3efc6e9f-cfdb-41c8-a02c-5968aaf7fa07.png)


# References 💻

+ [GitHub](https://github.com/anushakuppahally/spotify-api-project) Spotify API Project
+ [DataCamp](https://www.datacamp.com/tutorial/recommender-systems-python) Recommender systems in python
+ [Dashboard Spotify](https://developer.spotify.com/dashboard/) Spotify dashboard
+ [Developer Spotify](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlists-tracks) Documentation Spotipy
+ [PythonGuis](https://www.pythonguis.com/tutorials/create-gui-tkinter/) GUI Tkinter

# License ©️

This project is licensed under the MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.


