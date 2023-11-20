import requests
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, set_appearance_mode, set_default_color_theme, \
    CTkProgressBar
from pytube import YouTube
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Logo = resource_path("Logo.png")


def download_video():
    try:
        link = entry_link.get()
        yt = YouTube(link, on_progress_callback=on_progress)
        vid = yt.streams.get_highest_resolution()

        # Specify the target directory (in this case, "Video" folder)
        target_directory = os.path.join(os.path.expanduser("~"), "Video")
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        # Save the video to the target directory
        vid.download(output_path=target_directory)

        label_downloaded.configure(text=f'Video saved to {str(target_directory)}')
    except Exception as e:
        label_info.configure(text=f'An error occurred: {e}', text_color='red')


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    label_percentage.configure(text=per+'%')
    download_progress.update()
    download_progress.set(float(percentage_of_completion)/100)


def get_video_size(url):
    response = requests.head(url)
    size_bytes = int(response.headers.get('content-length', 0))
    size_mb = size_bytes / 1000000
    return size_mb


def check_video():
    try:
        vid_link = entry_link.get()
        yt = YouTube(vid_link)
        vid_title = yt.title
        size_mb = get_video_size(vid_link)
        label_info.configure(text=f'Title: {vid_title}\nSize: {size_mb:.2f} MB', text_color='white')
    except Exception as e:
        label_info.configure(text=f"Error occurred: {e}", text_color='red')


# window
root = CTk()
root.geometry('600x650')
root.title('YtDownloader')


# appearance
set_appearance_mode('Dark')
set_default_color_theme('blue')


# grid
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

# label
label_link = CTkLabel(master=root, text='Entry youtube link', font=('Arial', 24))
label_link.grid(row=0, column=0, sticky='nsew', padx=20, pady=15)
label_percentage = CTkLabel(master=root, text='0%')
label_percentage.grid(row=3, column=0, sticky='n')
label_info = CTkLabel(master=root, text='', font=('Arial', 18), wraplength=400)
label_info.grid(row=2, column=0)
label_downloaded = CTkLabel(master=root, text='')
label_downloaded.grid(row=2, column=0, sticky='s')

# entry
entry_link = CTkEntry(master=root, width=400, height=45, corner_radius=15, text_color='white', font=('Arial', 20))
entry_link.grid(row=1, column=0, sticky='new', padx=20, pady=15)

# buttons
download_button = CTkButton(master=root, command=download_video, width=40, height=40, corner_radius=10, text='Download')
download_button.grid(row=1, column=0, padx=(5, 120), pady=10)

check_button = CTkButton(master=root, command=check_video, width=40, height=40, corner_radius=10, text='Check')
check_button.grid(row=1, column=0, padx=(120, 5), pady=10)

# progress bar
download_progress = CTkProgressBar(root, orientation='horizontal', height=15, width=400, progress_color='green')
download_progress.grid(row=3, column=0, pady=10, padx=20)
download_progress.set(0)

# run
root.mainloop()
