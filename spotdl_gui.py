# NECESSARY IMPORTS

# Installs Spotify-downloader if not installed already.
try:
    import spotdl
except:
    if input("Spotdl not found, download now? (y/n)").lower() == 'y':
        system('pip install -U spotdl')
    else:
        sys.exit()
        
from tkinter import messagebox, filedialog
from os import system
import sys
import spotdl
from spotdl import Spotdl, util
from spotdl.authorize.services import AuthorizeSpotify
from spotdl.helpers.spotify import SpotifyHelpers
import tkinter as tk
from tkinter import *
import sys
from threading import Thread




helper_instance = SpotifyHelpers(spotify=AuthorizeSpotify(client_id='4fe3fecfe5334023a1472516cc99d805',
                                                          client_secret='0f02b7c483c04257984695007a4a8d5c'))


def Widgets():
    # Link Box
    link_label = Label(root, text="Spotify Link :", bg="#E8D579")
    link_label.grid(row=1, column=0, pady=5, padx=5)
    root.linkText = Entry(root, width=55, textvariable=song_link)
    root.linkText.grid(row=1, column=1, pady=5, padx=5, columnspan=2)

    # Directory Selector and Browse Button
    destination_label = Label(root, text="Destination   :", bg="#E8D579")
    destination_label.grid(row=2, column=0, pady=5, padx=5)
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

    global log_widget
    log_widget = Text(master=root, height=1, width=50)
    log_widget.grid(row=8, columnspan=3, padx=3, pady=3)
    log_widget.configure(state='disabled')
    


def logs():
    print(util.install_logger(level=log.get()))


printLog = Thread(target=logs)


def logwrite_begin():
    log_widget.configure(state='normal')
    log_widget.insert(END, 'Downloading, Check Console For Logs/Progress')
    log_widget.configure(state='disabled')


def logwrite_end():
    log_widget.configure(state='normal')
    log_widget.delete(1.0, END)
    log_widget.insert(
        END, "Download Complete, Check Console for Logs/Errors.")
    log_widget.configure(state='disabled')

# Function For Browse Button


def Browse():
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH")
    download_Path.set(download_Directory)


def song():
    logwrite_begin()
    printLog.start()

    def download():
        spotdl_instance.download_track(song_link.get())
        logwrite_end()
    downloader = Thread(target=download)
    downloader.start()


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


def textlist():
    logwrite_begin()
    printLog.start()

    def download():
        spotdl_instance.download_tracks_from_file(song_link.get())
        logwrite_end()
    downloader = Thread(target=download)
    downloader.start()


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
