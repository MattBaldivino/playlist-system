# -*- coding: utf-8 -*-
"""CS 3560 Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XU82rU2cKDygnliFh_PdQhfFHIL63xVj
"""
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from dotenv import load_dotenv
import spotipy
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector 
import os
import random
from api import getSong, playSong, ms_to_mins_secs, pauseSong

# Note: methods are not all compilable, *** is used to note the methods/use cases that need work


mydb = mysql.connector.connect(
    host = "DESKTOP-1HPMV6C",
    user = "root",
    database = "playlist",
) 
cursor = mydb.cursor()


class Song:
  def __init__(self, name, artist, duration, song_id): #genre used for recommendations
    self._song_id = song_id
    self._song_name = name
    self._song_artist = artist
    self._song_duration = duration
  
  @property
  def song_id(self):
    return self._song_id
  
  @property
  def song_name(self):
    return self._song_name
  
  @property
  def song_artist(self):
    return self._song_artist
  
  @property
  def song_duration(self):
    return ms_to_mins_secs(int(self._song_duration))
  
  def __str__(self):
    return self._song_name
  
class FriendRequest:
  def __init__(self, sender, recipient):
      self.sender = sender
      self.recipient = recipient
      DataBase.sendFriendRequestFromDB(sender, recipient)


class Account:
  # Method to create an account ***
  def __init__(self, username, password):
    self._username = username
    self._password = password
    self._friend_list = []
    self._playlists = []
    self._account_ID = 0

  # Sending a friend request ***
  def send_fr(username):
    if username: # If username exists in system
      # -> Send accept_fr to other 
      return None

  # Responding to a friend request ***
  def accept_fr():
    response = input("X has sent you a friend request: Would you like to accept or decline?")
    if (response == "Accept"):
      friendlist.append(username)
      return "You and user are now friends"
    else:
      return "You have declined the request"

  def getUsername(self):
    return self._username
  
  def getPassword(self):
    return self._password
  
  def playlists(self):
    val = self._account_ID
    command = ("SELECT playlist_ID FROM Playlist WHERE user_ID = '%s';")
    command.execute(command, val)
    playlists = cursor.fetchall()
    return playlists 
  # Sends account data to the table in database 
  def accountToDataBase(self):
    DataBase.addAccount(self._username, self._password)
  
  
# Create subclass of music playlist for an account
class MusicPlaylist:
  # Method to create a playlist ***
  def __init__(self, playlist_name):
    self._songs = []
    self._playlist_name = playlist_name
    self._length = 0
    self._duration = 0
    self._current_song = None
    self._playing = False
    self._playlist_ID = 0

  @property
  def songs(self):
    return self._songs

  @property
  def playlist_name(self):
    return self._playlist_name
    
  @playlist_name.setter
  def playlist_name(self, value):
    self._playlist_name = value

  @property
  def length(self):
    return self._length
    
  @length.setter
  def length(self, value):
    self._length = value

  @property
  def duration(self):
    return ms_to_mins_secs(self._duration)
  
  @property
  def current_song(self):
    return self._current_song
    
  @current_song.setter
  def current_song(self, value):
    self._current_song = value

  @property
  def playing(self):
    return self._playing
  
  @playing.setter
  def playing(self, value):
    self._playing = value

  #takes a tuple containing song name, artist, duration, and id as input
  #Sends song data to song table in database
  def add_song(self, song):
    new_song = Song(song[1], song[2], song[3], song[0])
    self._songs.append(new_song)
    self._length = self._length + 1
    self._duration = self._duration + song[3]
    DataBase.addSongsToDB(song[1], song[2], song[3], song[0])

  #calls spotify api to search by name
  def search_song(self, name):
    search = getSong(name)
    return search

  #print elements in song list
  def display_songs(self):
    for song in self.songs:
      print(song)

  #returns a song object
  def get_song(self, index):
    return self.songs[int(index)]
  
  # Play a song based off it's index in the playlist***
  def play(self, playlist_index):
    now_playing = self.get_song(playlist_index)
    self.current_song = playing_index
    self.playing = True
    playSong(now_playing.song_id)
    return None

  # Pause a song ***
  def pause(self):
    # Insert media player to pause a song
    pauseSong()
    return None

  # Skip a song ***
  def skip(self):
    #if on the last song of the playlist, loop back to the first
    if(int(self.current_song) == int(self.length - 1)):
      self.current_song = 0
    else:
      #set current song to next song and play it
      self.current_song = int(self.current_song) + 1
    self.play(self.current_song)
    return None

  # Shuffle playlist ***
  def shuffle(self):
    random.shuffle(self.songs)

  # Automatically play the next song (temporal event) ***
  def play_next(pl):
    # When song finishes, play next song in queue
    return None

  # Share a playlist via link ***
  def share_pl(pl):
  # Update playlist record
    return None
  
  # Sends playlist data to playlist table in Database 
  def playlistToDataBase(self):
    DataBase.addPlaylistsToDB(self._playlist_name, self._length, self.length)

  def getFromDB(self,name, user_id):
    self._playlist_name = DataBase.getPlaylistNameFromDB(name, user_id)
    self._length = DataBase.getPlaylistLengthFromDB(DataBase.getPlaylistIDFromDB(name, user_id))
    self._duration = DataBase.getPlaylistDurationFromDB(DataBase.getPlaylistIDFromDB(name, user_id))
    self._playlist_ID = DataBase.getPlaylistIDFromDB(name, user_id)



  
#Methods that send songs to the database 
class DataBase:
  # Method that sends songs to song table in database
  def addSongsToDB(name, artist, duration, id):
    addSong = "INSERT INTO Song (Name, Artist, Duration, song_ID) VALUES (%s, %s, %s, %s)"
    song = (name, artist, duration, id)
    cursor.execute(addSong,song)
    mydb.commit()

  # Store list of all avalible accounts ***
  def addAccountsToDB(username, password):
    addAccount = "INSERT INTO User (Username, Password) VALUES (%s, %s)"
    account = (username, password)
    cursor.execute(addAccount, account)
    mydb.commit()

  # Store list of all public playlists ***
  def addPlaylistsToDB(name, length, duration):
    addPlaylist = "INSERT INTO User (Name, Length, Duration) VALUES (%s, %s, %s)"
    playlist = (name, length, duration)
    cursor.execute(addPlaylist, playlist)
    mydb.commit()

  # Store list of friend requests in Freind request Table
  def sendFriendRequestFromDB(usernameOne, usernameTwo):
    val = (usernameOne.getAccountIDFromDB, usernameTwo.getAccountIDFromDB)
    command = "INSERT INTO FriendRequest (user_ID, friend_ID) VALUES (%s, %s)"
    cursor.execute(command, val)
    mydb.commit()

  # Adds freinds from friend Request Table to Friends
  def addFriendFromDB(usernameOne, usernameTwo, acceptance):
    val = (usernameOne.getAccountIDFromDB, usernameTwo.getAccountIDFromDB)
    if acceptance == True :
      command = "UPDATE FriendRequest SET Added = 1; INSERT INTO Friends (user_ID, friend_ID) VALUES (%s, %s);"
      cursor.execute(command,val)
      mydb.commit()
    else :
      command = "DELETE FROM FreindRequest WHERE user_ID = '%s' AND friend_ID = '%s';"
      cursor.execute(command,val)
      mydb.commit()

  # Stores all Songs from a Playlist
  def addToPlaylist(songName, playlistName, username):
    val = (playlistName.getPlaylistIDFromDB(playlistName, username.getAccountIDFromDB(username)),songName.getSongID(songName))
    command = "INSERT INTO Playlist_Songs (playlist_ID, song_ID) VALUES ('%s', '%s')"
    cursor.execute (command, val)
    mydb.commit()

  #All getters and setters for the DataBase
  def getSongNameFromDB(name, id):
    val = (name, id)
    command = "SELECT Name FROM Song WHERE Name = '%s' AND song_ID = '%s';"
    songName = cursor.execute(command, val)
    return songName
  
  def getSongArtistFromDB(artist, id):
    val = (artist, id)
    command = "SELECT Artist FROM Song WHERE Artist = '%s' AND song_ID = '%s';"
    songArtist = cursor.execute(command, val)
    return songArtist
  
  def getSongDurationFromDB(duration, id):
    val = (command, id)
    command = "SELECT Duration FROM Song WHERE Name = '%s' AND song_ID = '%s';"
    songDuration = cursor.execute(command, val)
    return songDuration
  
  def getSongID(name):
    command = "SELECT song_ID FROM Song WHERE Name = '%s';"
    song_ID = cursor.execute(command, name)
    return song_ID
  
  def getPlaylistNameFromDB(name, id):
    val = (name, id)
    command = "SELECT Name FROM Playlist WHERE Name = '%s' AND user_ID = '%s';"
    playlistName = cursor.execute(command, val)
    return playlistName
  
  def getPlaylistLengthFromDB(id):
    val = (id)
    command = "SELECT Length FROM Playlist WHERE playlist_ID = '%s';"
    playlistLength = cursor.execute(command, val)
    return playlistLength
  
  def getPlaylistDurationFromDB(id):
    val = (id)
    command = "SELECT Duration FROM Playlist WHERE playlist_ID = '%s';"
    playlistLength = cursor.execute(command, val)
    return playlistLength
  
  def getPlaylistIDFromDB(name, id):
    val = (name, id)
    command = "SELECT Name FROM Playlist WHERE Name = '%s' AND user_ID = '%s';"
    playlist_ID = cursor.execute(command,val)
    return playlist_ID
  
  def newPlaylistLength(length,id):
    val = (length, id)
    command = "UPDATE Playlist SET Length = '%s' WHERE playlist_ID = '%s';"
    cursor.execute(command,val)
    mydb.commit()
  
  def getAccountNameFromDB(name, id):
    val = (name, id)
    command = "SELECT Username FROM User WHERE Username = '%s';"
    accountName = cursor.execute(command, val)
    return accountName

  def getAccountIDFromDB(name):
    val = (name)
    command = "SELECT user_ID FROM User WHERE Username = '%s';"
    accountID = cursor.execute(command, val)
    return accountID

  def getFriendRequestFromDB(username):
    command = "SELECT friend_ID FROM FriendRequest WHERE user_ID = '%s';"
    requestList = cursor.execute(command, username.getAccountIDFromDB)
    return requestList

  def getFriendsFromDB(self):
    command = "SELECT friend_ID FROM Friends WHERE user_ID = '%s';"
    friendList = cursor.execute(command , self.getAccountIDFromDB)
    return friendList
  
  def getSongsFromPlaylist(id):
    command  = "SELECT Song_ID FROM Playlist_Songs WHERE playlistID = '%s';"
    songList = cursor.execute(command,id)
    return songList

   
""" if __name__ == "__main__":
  #TESTING PLAYLIST METHODS
  my_pl = MusicPlaylist("Playlist 1")

  search = input("What song would you like to add to the playlist? ")
  query = my_pl.search_song(search)
  #returns list of tuples containing the top 10 search results for the given song name
  print(query)
  selection = input("which index would you like to add to the playlist? ")
  #add the desired search result to the playlist
  my_pl.add_song(query[int(selection)])

  print("\n")

  search = input("What song would you like to add to the playlist? ")
  query = my_pl.search_song(search)
  #returns list of tuples containing the top 10 search results for the given song name
  print(query)
  selection = input("which index would you like to add to the playlist? ")
  #add the desired search result to the playlist
  my_pl.add_song(query[int(selection)])

  my_pl.display_songs()

  my_pl.shuffle()

  my_pl.display_songs()
 """
  

# *************** Login Screen **************************
class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Screen")
        self.geometry("1600x900")

        #create each frame within the app class
        #pack() function used to display elements on screen

        ##
        #LOGIN FRAME
        ##
        self.login_frame = tk.Frame(self)
        username_label = tk.Label(self.login_frame, text = "Username:")
        username_label.pack()

        username_entry = tk.Entry(self.login_frame)
        username_entry.pack()

        password_label = tk.Label(self.login_frame, text = "Password:")
        password_label.pack()

        password_entry = tk.Entry(self.login_frame, show ="*")
        password_entry.pack()

        #command used to call functions within the program
        login_button = tk.Button(self.login_frame, text = "Login", command = self.to_mainMenu)
        login_button.pack()

        register_label = tk.Label(self.login_frame, text = "Don't have an account?")
        register_label.pack()

        register_button = tk.Button(self.login_frame, text = "Register", command = self.to_register)
        register_button.pack()



        ##
        #REGISTER FRAME
        ##
        self.register_frame = tk.Frame(self)
        username_label = tk.Label(self.register_frame, text = "Username:")
        username_label.pack()

        username_entry = tk.Entry(self.register_frame)
        username_entry.pack()

        password_label = tk.Label(self.register_frame, text = "Password:")
        password_label.pack()

        password_entry = tk.Entry(self.register_frame, show ="*")
        password_entry.pack()

        password_label2 = tk.Label(self.register_frame, text = "Confirm Password:")
        password_label2.pack()

        password_entry2 = tk.Entry(self.register_frame, show ="*")
        password_entry2.pack()

        register_button = tk.Button(self.register_frame, text = "Register", command = self.to_login)
        register_button.pack()

        self.login_frame.pack()

# --------------------------------Login Screen Functions ---------------------------------------------------
    def to_mainMenu(self):
        self.withdraw()
        self.main_menu = MainMenu()

    def to_register(self):
        #forget the current frame/screen
        self.login_frame.forget()
        #show the register frame/screen
        self.title("Register Screen")
        self.register_frame.pack()

    def to_login(self):
        self.register_frame.forget()
        self.title("Login Screen")
        self.login_frame.pack()








class MainMenu(tk.Tk):
    # *************** Main Menu **************************
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Main Menu')
        self.geometry('1600x900')

        ######## Main Menu Frame ##########################################################################
        self.mm_frame = tk.Frame(self)
        
        #******** Left Side Functions *************************************
        left_frame = tk.Frame(self.mm_frame)
        # Pack the frame to the left side of the main frame
        left_frame.pack(side='left', fill='both')
        

        # "Your Playlists Title + List of your Playlists"
        self.playlistsLabel = tk.Label(left_frame, text='Your Playlists', font='Arial 14')
        self.playlistsLabel.pack(side='top', fill='x')

        self.playlist = tk.Listbox(left_frame, width = 50, height = 30)
        self.playlist.pack(side='top', fill='both')

        # Back button
        self.back_button = tk.Button(left_frame, text = 'Return to Login', command = self.to_login)
        self.back_button.pack(side = 'bottom', pady=10)


        #******** Right Side Functions *************************************
        right_frame = tk.Frame(self.mm_frame)
        # Pack the frame to the right side of the main frame
        right_frame.pack(side='right', fill = 'both')

        # "Your Friend List Title + List of your Friends"
        self.friendslistLabel = tk.Label(right_frame, text='Friend List', font = 'Arial 14')
        self.friendslistLabel.pack(side='top', fill = 'x')

        self.friendslist = tk.Listbox(right_frame, width = 50, height = 30)
        self.friendslist.pack(side='top', fill = 'both')


        #******** Middle Functions *************************************
        middle_frame = tk.Frame(self.mm_frame)

        # Pack the frame to the middle of the main frame
        middle_frame.pack(side='top', fill='both')

        # Main Menu Title
        self.mainMenuLabel = tk.Label(middle_frame, text='Main Menu', font = 'Arial 18')
        self.mainMenuLabel.pack()

        # Create Playlist Button
        self.createPlaylist = tk.Button(middle_frame, text='Create Playlist', font = 'Arial 14', height=10, width=20, command = self.create_playlist) # command = create_playlist
        self.createPlaylist.pack(expand = True, padx=30)
        
        # Add Friend Button
        self.addFriend = tk.Button(middle_frame, text='Add Friend', font = 'Arial 14', height=10, width=20, command = self.add_friend) # command = add_friend
        self.addFriend.pack(expand = True, padx=30)

        # Go to Search Screen Button
        self.SearchButton = tk.Button(middle_frame, text='Search for Playlists', font = 'Arial 14', height=12, width=20, command=self.to_Search_Screen) # command = to_Search_Screen
        self.SearchButton.pack(expand = True, padx=30)

        self.mm_frame.pack(fill='both')


# --------------------------------Main Menu Functions ---------------------------------------------------
    def create_playlist(self):
        # Create a new frame in the main window
        self.create_frame = tk.Frame(self)

        # Create a label and a text box entry
        label = tk.Label(self.create_frame, text="Enter a playlist name:")
        label.pack()
        entry = tk.Entry(self.create_frame)
        entry.pack()
        # Create a confirmation button
        confirm_button = tk.Button(self.create_frame, text="Create Playlist", command=lambda: self.to_playlist(entry.get()))
        confirm_button.pack()

        # Create a cancel button
        cancel_button = tk.Button(self.create_frame, text="Cancel", command=self.to_main_menu)
        cancel_button.pack()

        # Remove the main menu functions and open the create_frame
        self.mm_frame.forget()
        self.create_frame.pack(fill="both", expand=True)

    # Return to main menu
    def to_main_menu(self):
        self.create_frame.forget()
        self.mm_frame.pack(fill='both', expand=True)

    # Go to Playlist
    def to_playlist(self, entry):
        if (entry == ""): # Error message when playlist name is empty
            error = tk.Toplevel(self)
            error.title("Error")
            error.geometry("200x100")
            label = tk.Label(error, text="Please give your playlist a name")
            label.pack()
        else:
            self.new_playlist = YourPlaylist(self, entry)
            self.playlist.insert(tk.END, entry)

    # Return to login
    def to_login(self):
        self.withdraw()
        self.login = Login()

    # Go to search
    def to_Search_Screen(self):
        self.search = Search()


############################################################################
# Test for friend request function
    user_data = {}

    # Add friend
    def add_friend(self):
    # Create a new window
        window = tk.Toplevel()
        window.geometry('500x300')
        # Create a label and an entry widget
        label = tk.Label(window, text="Enter username:")
        label.pack()
        entry = tk.Entry(window)
        entry.pack()

        # Create a confirmation button
        confirm_button = tk.Button(window, text="Add Friend", command=lambda: self.send_fr(entry.get()))
        confirm_button.pack()

        # Create a cancel button
        cancel_button = tk.Button(window, text="Cancel", command=window.destroy)
        cancel_button.pack()

    # Check for user
    def check_user(username, requester):
        if username in user_data:
            # Send a friend request to the user
            user_data[username]['friend_requests'].append(requester)
        else:
            # Print an error message
            print(f"User not found: {username}")

    # Send Friend Request        
    def send_fr(username):
        if username in user_data:
        # Send a friend request to the user
            check_user(username, self.username)
            print(f"Friend request sent to {username}")
        else:
            print(f"User not found: {username}")

    # Accept Friend Request
    def accept_friend_request(self, requester):
        # Condition: username exists and requester inputs their name 
        if self.username in user_data and requester in user_data[self.username]['friend_requests']:
        # 1) Remove the friend request from the user's list of friend requests
            user_data[self.username]['friend_requests'].remove(requester)

        # 2) Add the requester as a friend of the user
            if 'friends' not in user_data[self.username]:
                user_data[self.username]['friends'] = []
            user_data[self.username]['friends'].append(requester)

        # 3) Add the user as a friend of the requester
            if 'friends' not in user_data[requester]:
                user_data[requester]['friends'] = []
            user_data[requester]['friends'].append(self.username)
            # Accept Message
            print(f"Friend request accepted from {requester}")

    # Decline Friend Request
    def reject_friend_request(self, requester):
        if self.username in user_data and requester in user_data[self.username]['friend_requests']:
        # Remove the friend request from the user's list of friend requests
            user_data[self.username]['friend_requests'].remove(requester)
            # Decline Message
            print(f"Friend request rejected from {requester}")
            


              
# *************** Playlist Class **************************
class YourPlaylist(tk.Toplevel):
    def __init__(self, master, name = None):
        tk.Toplevel.__init__(self, master)
        self.name = name
        self.title(name)
        self.geometry('1600x900')
        label = tk.Label(self, text=f"{self.name}")
        label.pack()
        ######## Playlist Frame ##########################################################################
        self.playlist_frame = tk.Frame(self)

        # Display Headings (Title/Artist/Duration Headings)
        self.table = ttk.Treeview(self.playlist_frame, columns=('title', 'artist', 'duration'), show='headings')
        self.table.heading('title', text='Song Title')
        self.table.heading('artist', text='Artist')
        self.table.heading('duration', text='Duration')
        self.table.pack(fill='both', expand = True)

        self.title_label = ttk.Label(master=self.playlist_frame, font='Arial 18')
        self.title_label.pack()

        ################## Test Spotify API Here #############################
        load_dotenv()
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        redirect_uri = os.getenv("REDIRECT_URI")


        # Display Buttons at bottom

        button_frame = tk.Frame(self.playlist_frame)
        self.play_button = tk.Button(button_frame, text = 'Play', command=self.play)
        self.search_button = tk.Button(button_frame, text = 'Search', command=self.to_search)

        # Pack the buttons into the frame and center them
        self.play_button.pack()
        self.search_button.pack()
        button_frame.pack(fill='both', expand=False)

        self.playlist_frame.pack(fill='both', expand = True)

    def item_select(self, _):
        print(self.table.selection())
        for i in self.table.selection():
            print(self.table.item(i)['values'])

    def delete_song(self):
        print('Song has been removed')
        for i in self.table.selection():
            self.table.delete(i)

    def play(self, song_uri):
        playback_state = self.sp.current_playback()

        # If the user is not currently playing a song, start a new playback
        if playback_state is None or playback_state['is_playing'] is False:
            self.sp.start_playback(uris=[song_uri])
        # If the user is already playing a song, add the new song to the queue
        else:
            self.sp.add_to_queue(song_uri)
        # Play the song
        self.sp.next_track()

    def to_search(self):
        self.search = Search()



class Search(Tk):
    # *************** Search Screen **************************
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Search Screen')
        self.geometry("1600x900")
        search_label = Label(self, text="Search for music.")
        search_label.pack()

        search_bar = Entry(self)
        search_bar.pack()

        result_list = Listbox(self)
        result_list.pack()

        #on event, run the specified function
        search_bar.bind("<Return>", check)
        result_list.bind("<<ListboxSelect>>", play_selected)

# --------------------------------Main Menu Functions ---------------------------------------------------
        def update(data):
            result_list.delete(0, END)

            for item in data:
                result_list.insert(END, (item[2] + " - " + item[1]))

        def check(e):
            typed = search_bar.get()
            update(getSong(typed))

        def play_selected(e):
            typed = search_bar.get()
            songs = getSong(typed)
            selected = result_list.curselection()
            playSong(songs[selected[0]][0])