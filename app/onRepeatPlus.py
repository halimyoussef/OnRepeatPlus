import pandas as pd
from tkinter import *
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyService():
    def __init__(self):
        spotify_cid = '' #TODO : put your own spotify client id
        spotify_secret = '' #TODO : put your own spotify secret id
        spotify_redirect_uri = 'https://google.com'
        scope = "playlist-read-private"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_cid, client_secret=spotify_secret,
                                                       redirect_uri=spotify_redirect_uri, scope=scope))

    def getPlaylistsSongs(self, id):
        """
        Fetch the id, name, artist and link to all of the songs in a SPotify playlist
        :param id: String (id of the playlist)
        :return: DataFrame (all the songs and audio features of a playlist)
        """
        print('>>> Starting a search for songs...')
        try:
            results = self.sp.playlist_items(playlist_id=id)
            songs = results['items']
            print(songs)
            page = 1
            while results['next']:
                print('>>> Page n°' + str(page))
                results = self.sp.next(results)
                songs.extend(results['items'])
                page+=1

            # We get all the songs in the playlist 'On Repeat' and only keep the information that are useful
            songsInfo = {'id': [], 'name': [], 'artist': [], 'lien':[]}
            step = 1
            for idx, item in enumerate(songs):
                try:
                    id = item['track']['id']
                    name = item['track']['name']
                    artist = item['track']['artists'][0]['name']
                    url = item['track']['external_urls']['spotify']

                    print(id,name,artist,url, sep="---")

                    songsInfo['id'].append(id)
                    songsInfo['name'].append(name)
                    songsInfo['artist'].append(artist)
                    songsInfo['lien'].append(url)
                    print('>>> Song extraction n°' + str(step))
                    step+=1
                except:
                    pass

            # We create a dataFrame with the data we got
            dfSongs = pd.DataFrame(songsInfo)
            dfSongs = dfSongs.drop_duplicates(subset=['id'])
            print('>>> Songs harvested !')
            return  dfSongs
        except Exception as r:
            return 'There was an error, please try again with another id'

    def addAudioFeatures(self, df):
        """
        Fetch the audiofeatures of the songs in a dataset and merge them together
        :param df: dataframe of the songs
        :return: dataframe of the songs with their audiofeatures
        """
        print('>>> Starting audio analysis...')
        songFeatures = {'id': [], 'danceability': [], 'energy': [], 'key': [], 'loudness': [],
                        'speechiness': [], 'acousticness': [], 'instrumentalness': [],
                        'liveness': [], 'valence': [], 'tempo': []}
        step = 1
        for idx, row in df.iterrows():
            try:
                af = self.sp.audio_features(row[0])
                songFeatures['id'].append(af[0].get('id'))
                songFeatures['danceability'].append(af[0].get('danceability'))
                songFeatures['energy'].append(af[0].get('energy'))
                songFeatures['key'].append(af[0].get('key'))
                songFeatures['loudness'].append(af[0].get('loudness'))
                songFeatures['speechiness'].append(af[0].get('speechiness'))
                songFeatures['acousticness'].append(af[0].get('acousticness'))
                songFeatures['instrumentalness'].append(af[0].get('instrumentalness'))
                songFeatures['liveness'].append(af[0].get('liveness'))
                songFeatures['valence'].append(af[0].get('valence'))
                songFeatures['tempo'].append(af[0].get('tempo'))
                print('>>> Audio analysis n°' + str(step))
                step+=1
            except:
                pass
        # We create a dataFrame with the data we got
        dfFeatures = pd.DataFrame(songFeatures)
        dfSongsFeatures = pd.merge(df, dfFeatures, on='id')
        print('>>> Audio analysis done !')
        return dfSongsFeatures

    def getSongsAndFeatures(self, id):
        """
        Fetch the songs and their audio features at the same time into a dataset
        :param id: playlist id
        :return: dataframe of the songs with their audiofeatures
        """
        print('>>> Starting song harvesting and audio analysis...')
        songs = self.getPlaylistsSongs(id)
        songsAndFeatures = self.addAudioFeatures(songs)
        print('>>> Song harvesting and audio analysis done !')
        return songsAndFeatures

    def getCurrentOnRepeat(self):
        """
        Returns all audio features, name, artist and id of the current top songs
        on repeat in a dataframe
        :return: DataFrame (Top 30 on repeat songs and audio features)
        """
        print('>>> Starting OnReapeat Playlist harvesting...')
        return self.getSongsAndFeatures('37i9dQZF1EpeFTsZYFTRZQ')

def removeNaNFeatures(df):
    """
    Removes all the NaN features of the merged datasets.
    :param df: dataframe with both
    :return: dataframe with only the audio features
    """
    print('>>> Removing NaN values...')
    df2 = df.drop(['id'], axis=1)
    df2 = df2.drop(['artist'], axis=1)
    df2 = df2.drop(['name'], axis=1)
    df2 = df2.drop(['lien'], axis=1)
    print('>>> NaN values removed')
    return df2

def saveAsCSV(df, csvName):
    """
    Saves a dataframe into a csv file
    :param df: dataframe to saved
    :param csvName: name of the file
    """
    print('>>> Creating ' + str(csvName) + ".csv ...")
    df.to_csv('data\\'+csvName)
    print('>>> CSV created !')

def getRecommandtionFromCSV(sample_csv, all_csv):
    """
    Get recommendations from reading two csv files.
    :param sample_csv: TOP30 songs dataset
    :param all_csv: DDB dataset
    :return: dataframe with 3x n#rows of sample_csv
    """
    print('>>> Searching for recommandations through CSV files...')
    df_sample = pd.read_csv('data\\'+sample_csv)
    df_tracks = pd.read_csv('data\\'+all_csv)
    print('>>> CSV files have been read.')
    return getRecommandation(df_sample, df_tracks)

def getRecommandation(df_sample, df_tracks):
    """
    Gets recommandations from two dataframes
    :param df_sample: TOP30 songs dataframe
    :param df_tracks: DDB dataframe
    :return: dataframe with 3x n#rows of df_sample
    """
    #we drop the first column created by read_csv
    print('>>> Starting recommendation search...')
    df_sample.drop(columns=df_sample.columns[0], axis=1, inplace=True)
    df_tracks.drop(columns=df_tracks.columns[0], axis=1, inplace=True)
    df_total = pd.concat([df_tracks, df_sample])

    #we calculate the cosine similarity of all the songs
    df_total_NaN = removeNaNFeatures(df_total)
    cosine_sim = cosine_similarity(df_total_NaN, df_total_NaN)
    print('>>> Overall cosine similarity calculated.')
    indices = pd.Series(df_total.index, index=df_total['id'])
    no = 1
    listReco = []

    for idx in df_sample.index:
        print('>>> Getting recommandations for song n° ' + str(no))
        id = df_sample['id'][idx]
        cos_idx = indices[id]
        sim_scores = list(enumerate(cosine_sim[cos_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:3]
        track_indices = [i[0] for i in sim_scores]
        recoID = df_total['id'].iloc[track_indices]
        recoOneSong = df_total.loc[df_total['id'].isin(recoID)]
        listReco.append(recoOneSong)
        no+=1

    total = pd.concat(listReco)
    recofinal = total.drop_duplicates(subset=["name", "artist"])
    print('>>> Recommendations found !')

    return recofinal

class SimpleGUI(Tk):
    """
    Class that will create a GUI for the application
    """
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
        Sets the size, name and color of the GUI
        :return:
        """
        self.title("Spotify recommandation")
        self.maxsize(1000, 800)
        self.config(bg="green")
        self.setupWindow()

    def setupWindow(self):
        """
        Setups the GUI and the different frame
        """

        #LEFT FRAME
        left_frame = Frame(self, width=200, height=650)
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nw')
        #RIGHT FRAME
        right_frame = Frame(self, width=750, height=650)
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky='nes')

        #LEFT SETTINGS
        Label(left_frame, text="Settings", font=20).grid(row=0, column=0, padx=5, pady=5)

        Label(left_frame, text='Do you want to update onRepeat data ?').grid(row=1, column=0, padx=5, pady=5,
                                                                             sticky='w')
        self.update_var = BooleanVar()
        Checkbutton(left_frame, text='YES', variable=self.update_var).grid(row=2, sticky='w')

        Label(left_frame, text='Please input the playlist ID you want to get rec from :'
                               '\n(Leave empty if you want to use the provided playlist\nType 1 to use the last input playlist)').grid(row=3, column=0, padx=5,
                                                                                                pady=5, sticky='w')
        self.playlist_id = Entry(left_frame)
        self.playlist_id.grid(row=4, column=0, padx=5, pady=5, sticky='w')

        Label(left_frame, text='Save results in a csv file ?').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.use_csv = BooleanVar()
        Checkbutton(left_frame, text='YES', variable=self.use_csv).grid(row=6, sticky='w')

        # BUTTONS
        Button(left_frame, text="Search", command=self.results).grid(row=7, column=0, padx=5, pady=5, sticky='w')
        Button(left_frame, text="Exit", command=self.close).grid(row=8, column=0, padx=5, pady=5, sticky='w')

        # RIGHT FRAME RESULT BOX
        self.listbox = Listbox(right_frame, width=80, height=40)
        self.listbox.pack(side=LEFT, fill=BOTH)
        scrollbar = Scrollbar(right_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

    def clearResult(self):
        """
        Clear the results in the right frame
        """
        if self.listbox.size() != 0:
            self.listbox.delete(0, END)

    def results(self):
        """
        Launch the SpotifyService class and the recommendation methods.
        Prints in a listbox all the songs recommended by the app.
        """
        self.clearResult()
        spoitfyService = SpotifyService()

        print('=============================')
        #UPDATE ONREAPEAT ?
        if self.update_var.get() is True:
            print('>>> Updating onRepeat data...')
            df_current_updated = spoitfyService.getCurrentOnRepeat()
            df_current_updated.to_csv('onRepeat.csv')
            print('>>> onRepeat data updated !')
        else:
            print('>>> Use current onRepeat data.')

        #RECOMMANDATION
        if len(self.playlist_id.get()) != 0:
            # REUSE LAST INPUT PLAYLIST
            if self.playlist_id.get() == '1':
                print('>>> Using last DDB input data...')
                df_reco = getRecommandtionFromCSV(sample_csv='onRepeat.csv', all_csv='ddbSpotifyInput.csv')
            else:
                try:
                    # CREATE A NEW INPUT PLAYLIST
                    print('>>> Creating new DDB data...')
                    df_specific = spoitfyService.getSongsAndFeatures(self.playlist_id.get())
                    df_specific.to_csv('ddbSpotifyInput.csv')
                    print('>>> New DDB saved into ddbSpotifyInput.csv')
                    df_reco = getRecommandtionFromCSV(sample_csv='onRepeat.csv', all_csv='ddbSpotifyInput.csv')
                except:
                    print('The ID is incorrect, please try again')
        else:
            # USE THE PROVIDED PLAYLIST
            print('>>> Use current DDB data.')
            df_reco = getRecommandtionFromCSV(sample_csv='onRepeat.csv', all_csv='ddbSpotify.csv')

        #CREATE A CSV FILE
        if self.use_csv.get() is True:
            print('>>> Saving recommandations into a csv file...')
            saveAsCSV(df_reco, 'reco.csv')
        else:
            print('>>> Recommandations not saved into a csv file...')

        #PRINT THE RESULTS IN THE RIGHT FRAME
        for idx, rows in df_reco.iterrows():
            song = rows['name']
            artist = rows['artist']
            lien = rows['lien']
            self.listbox.insert(END, '● '+ str(song) + ' by ' + str(artist))
            self.listbox.insert(END, lien)
            self.listbox.insert(END, '------------------------')

    def close(self):
        """
        Closes the application
        """
        self.quit()
        self.destroy()

if __name__ == '__main__':
    app = SimpleGUI()
    app.mainloop()

    #Playlist of 768 k-indie songs --> 3s2L74IrceQriyrkDlTtAf
