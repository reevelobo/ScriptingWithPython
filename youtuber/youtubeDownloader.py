from pytube import YouTube 
import tkinter as tk
from tkinter import filedialog

def download_vider(url, save_path):
    try: 
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True,file_extension="mp4")
        highest_res_stream = streams.get_highest_resolution()
        highest_res_stream.download(output_path=save_path)
        print("Video Download Successful")
    except Exception as e:
        print(e)

url = "https://www.youtube.com/watch?v=AwPiUIL8ep8"
save_path = "/Users/reevelobo/Desktop/Scripts/youtubeDownloader"

download_vider(url, save_path)





