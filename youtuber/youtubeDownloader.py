from pytube import YouTube 
import tkinter as tk
from tkinter import filedialog

def download_video(url, save_path):
    try: 
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True,file_extension="mp4")
        highest_res_stream = streams.get_highest_resolution()
        highest_res_stream.download(output_path=save_path)
        print("Video Download Successful")
    except Exception as e:
        print(e)

#
def open_file_dialog():
    folder= filedialog.askdirectory()
    if folder:
        print(f"Selected Folder : {folder}")
        return folder


# Specifies that you are directly running the python file before it executes anything under it 
if __name__=="__main__":
    root = tk.Tk()
    root.withdraw()

    vider_url = input("Please Enter the Youtube URL : ")
    save_dir = open_file_dialog()

    if not save_dir:
        print ("Invalid save location !!")
    else: 
        print("Started Download....")
        download_video(vider_url, save_dir)




