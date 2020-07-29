# NECESSARY IMPORTS
from tkinter import messagebox, filedialog
from os import system
import tkinter as tk
from tkinter import *
import sys


# Installs Spotify-downloader if not installed already.
try:
    import spotdl
except:
    if input("Spotdl not found, download now? (y/n)").lower() == 'y':
        system('pip install -U spotdl')
    else:
        sys.exit()


def Widgets():
    # Link Box
    link_label = Label(root, text="Spotify link :", bg="#E8D579")
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
    Download_B.grid(row=6, column=1, pady=3, padx=3)

    # Link Type Selection
    linkType_label = Label(root, text="Type :", bg="#E8D579")
    linkType_label.grid(row=4, column=0, pady=5, padx=5)
    typeList = ['song', 'playlist', 'album', 'list']
    link_type.set(typeList[0])
    opt2 = tk.OptionMenu(root, link_type, *typeList)
    opt2.config(width=10, bg="#05E8E0")
    opt2.grid(row=4, column=1, pady=3, padx=3)

    # Log Level Selection
    log_label = Label(root, text="Log Level :", bg="#E8D579")
    log_label.grid(row=5, column=0, pady=5, padx=5)
    logList = ["INFO", "DEBUG", "WARNING"]
    log.set(logList[0])
    opt = tk.OptionMenu(root, log, *logList)
    opt.config(width=10, bg="#05E8E0")
    opt.grid(row=5, column=1, pady=3, padx=3)

# Function For Browse Button
def Browse():
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH")
    download_Path.set(download_Directory)

# Function For Download Button
def Download():
    system(
        f'spotdl -{link_type.get()[0]} {song_link.get()} -f "{download_Path.get()}" -ll={log.get()}')
    messagebox.showinfo(message=f"Song(s)/text file saved to {download_Path.get()}\n"
                        "Check Console For Errors/Logs")


root = tk.Tk()

root.geometry("450x170")
root.resizable(False, False)
root.title("Spotify-Downloader")
root.config(background="#000000")

song_link = StringVar()
download_Path = StringVar()
log = StringVar()
link_type = StringVar()

Widgets()

root.mainloop()
