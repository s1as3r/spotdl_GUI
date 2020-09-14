# NECESSARY IMPORTS
from os import system
import tkinter as tk
from tkinter import *
import sys
from tkinter import messagebox, filedialog
import sys
from threading import Thread

# Install Spotify-downloader if not installed already.
try:
    import spotdl
except:
    if input("Spotdl not found, download now? (y/n)").lower() == 'y':
        system('pip install -U spotdl')
    else:
        sys.exit()

from spotdl import Spotdl, util
from spotdl.authorize.services import AuthorizeSpotify
from spotdl.helpers.spotify import SpotifyHelpers

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# -- As per Spotfiy API documentation --
# Make sure that you safeguard your application Client Secret at all times.
# Be aware, for example, that if you commit your code to a public repository like GitHub
# you will need to remove the Client Secret from your code before doing so.
u_client_id = ''
u_client_secret = ''


try:
    # Attempt to locate spotify secret keys from a local spotify_keys.txt file
    with open("spotify_keys.txt", "r+") as keys:
        contents = keys.readlines()
        if contents:
            contents = [key.strip() for key in contents] # Removal of newlines
            try:
                u_client_id = contents[0]
                u_client_secret = contents[1]
                print(BColors.OKGREEN + "Success: Found local spotify keys!" + BColors.ENDC)
            except IndexError:
                raise FileNotFoundError
        else:
            raise FileNotFoundError

except FileNotFoundError:
    # If keys are not found, allow the user to obtain the keys from spotify
    print(BColors.WARNING + "Warning: You are missing the client_id/secret which is required for the album/playlist features" + BColors.ENDC)
    print(BColors.WARNING + "You can obtain these keys by creating a quick app with Spotify" + BColors.ENDC)
    print("https://developer.spotify.com/dashboard/applications\n")

    # User is able to proceed without keys, which will limit some features
    if(input("Enter keys manually? (y/n): ").lower()[0] == "y"):

        # Note: Create a first call to the /autorize endpoint to validate if an API token was retrieved?
        u_client_id = input("Enter your client id:")
        u_client_secret = input("Enter your client secret:")

        # Keys will be saved for the future in a local text file
        with open("spotify_keys.txt", "w") as keys:
            keys.writelines([u_client_id + "\n", u_client_secret])
        print(BColors.OKGREEN + "Success: Your keys were saved for future use!" + BColors.ENDC)

    else:
        print(BColors.WARNING + "Warning: Cannot Proceed Without Keys! Exiting Now..." + BColors.ENDC)
        sys.exit()
except:
    raise

helper_instance = SpotifyHelpers(spotify=AuthorizeSpotify(client_id=u_client_id, client_secret=u_client_secret))

# Prefill download path
import os
from pathlib import Path
location = str(os.path.join(Path.home(), "Downloads"))


def Widgets():
    # Link Box
    link_label = Label(root, text="Spotify Link :", bg="#E8D579")
    link_label.grid(row=1, column=0, pady=5, padx=5)
    root.linkText = Entry(root, width=55, textvariable=song_link)
    root.linkText.grid(row=1, column=1, pady=5, padx=5, columnspan=2)
    root.linkText.focus_set() 

    # Directory Selector and Browse Button
    destination_label = Label(root, text="Destination   :", bg="#E8D579")
    destination_label.grid(row=2, column=0, pady=5, padx=5)
    download_path.set(location) 
    root.destinationText = Entry(root, width=40, textvariable=download_Path)
    root.destinationText.grid(row=2, column=1, pady=5, padx=5)
    browse_B = Button(root, text="Browse", command=Browse,
                      width=10, bg="#05E8E0")
    browse_B.grid(row=2, column=2, pady=1, padx=1)

    # Download Button
    Download_B = Button(root, text="Download",
                        command=Download, width=20, bg="#05E8E0")
    Download_B.grid(row=7, column=1, pady=3, padx=3)

    # Link Type Selection
    linkType_label = Label(root, text="Type :", bg="#E8D579")
    linkType_label.grid(row=4, column=0, pady=5, padx=5)
    typeList = ['song', 'playlist', 'album', 'list']
    link_type.set(typeList[0])
    opt2 = tk.OptionMenu(root, link_type, *typeList)
    opt2.config(width=10, bg="#05E8E0")
    opt2.grid(row=4, column=1, pady=3, padx=3)

    ext_label = Label(root, text="File Format :", bg="#E8D579")
    ext_label.grid(row=6, column=0, pady=5, padx=5)
    extList = ['mp3', 'flac', 'm4a', 'opus', 'ogg']
    output_ext.set(extList[0])
    opt3 = tk.OptionMenu(root, output_ext, *extList)
    opt3.config(width=10, bg="#05E8E0")
    opt3.grid(row=6, column=1, pady=3, padx=3)

    # Log Level Selection
    log_label = Label(root, text="Log Level :", bg="#E8D579")
    log_label.grid(row=5, column=0, pady=5, padx=5)
    logList = ["INFO", "DEBUG", "WARNING", "ERROR"]
    log.set(logList[0])
    opt = tk.OptionMenu(root, log, *logList)
    opt.config(width=10, bg="#05E8E0")
    opt.grid(row=5, column=1, pady=3, padx=3)

    # State of the Script (Downloading/Completed Download)
    global log_widget
    log_widget = Text(master=root, height=1, width=50)
    log_widget.grid(row=8, columnspan=3, padx=3, pady=3)
    log_widget.configure(state='disabled')


# Function for getting the logs.
def logs():
    print(util.install_logger(level=log.get()))

# Running logs function on a different thread. Else, the UI would freeze.
printLog = Thread(target=logs)


# Prints downloading onto the status widget.
def logwrite_begin():
    log_widget.configure(state='normal')
    log_widget.insert(END, 'Downloading, Check Console For Logs/Progress')
    log_widget.configure(state='disabled')


# Prints download complete onto the status widget.
def logwrite_end():
    log_widget.configure(state='normal')
    log_widget.delete(1.0, END)
    log_widget.insert(
        END, "Download Complete, Check Console for Logs/Errors.")
    log_widget.configure(state='disabled')


# Function for the browse button.
def Browse():
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH")
    download_Path.set(download_Directory)

# Function for downloading a single track.
def song():
    logwrite_begin()
    printLog.start()

    def download():
        spotdl_instance.download_track(song_link.get())
        logwrite_end()
    downloader = Thread(target=download)
    downloader.start()


# Function for downloading an album.
def album():
    logwrite_begin()
    printLog.start()
    alb = helper_instance.fetch_album(song_link.get())
    helper_instance.write_album_tracks(alb, './album_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('album_tracks.txt')
        logwrite_end()
    downloader = Thread(target=download)
    downloader.start()


# Function for downloading a Playlist.
def playlist():
    logwrite_begin()
    printLog.start()
    playlist = helper_instance.fetch_playlist(song_link.get())
    helper_instance.write_playlist_tracks(playlist, '.\playlist_tracks.txt')

    def download():
        spotdl_instance.download_tracks_from_file('playlist_tracks.txt')
        logwrite_end()
    downloader = Thread(target=download)
    downloader.start()


# Function for downloading a list of songs from a .txt file.
def textlist():
    logwrite_begin()
    printLog.start()

    def download():
        spotdl_instance.download_tracks_from_file(song_link.get())
        logwrite_end()
    downloader = Thread(target=download)
    downloader.start()


# Function for the download button.
def Download():
    global spotdl_instance

    spotdl_instance = Spotdl(args={'output_file': download_Path.get(),
                                   'output_ext': output_ext.get()})
    if link_type.get() == 'song':
        song()
    elif link_type.get() == 'list':
        textlist()
    elif link_type.get() == 'playlist':
        playlist()
    elif link_type.get() == 'album':
        album()



root = tk.Tk()

root.geometry("440x250")
root.resizable(False, False)
root.title("Spotify-Downloader")
root.config(background="#000000")

song_link = StringVar()
download_Path = StringVar()
log = StringVar()
output_ext = StringVar()
link_type = StringVar()

Widgets()

root.mainloop()
