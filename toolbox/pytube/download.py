from pytube import YouTube
from pytube import Playlist
import os
import glob

# constant
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PROGRESS = 0

# what is already downloaded
present_files = os.listdir(BASE_DIR)
present_titles = [os.path.splitext(f)[0] for f in os.listdir(BASE_DIR)]

pl = Playlist('https://www.youtube.com/playlist?list=PLsXoa0ATE8k3jj2UV4bYDRh-CGN1nU586')
video_links = pl.parse_links()
video_links.reverse()
video_links = [f'http://youtube.com{x}' for x in video_links]

# where to start download
# video_links = video_links[:21]


def progress_function(stream, chunk, file_handle, bytes_remaining):
    percentage = (1-bytes_remaining / video.filesize) * 100
    ip = int(percentage)
    global PROGRESS
    if ip >= PROGRESS + 10:
        print(ip, '% done...')
        PROGRESS = ip


for link in video_links:
    try:
        yt = YouTube(link, on_progress_callback=progress_function)
        streams = yt.streams
        title = yt.title

        if title in present_titles:
            print(f'skipping... {title}')
            continue
        else:
            print(f'downloading... {title}')
            video = streams \
                .filter(only_audio=False).first()
                # .order_by('resolution') \
                # .desc() \
            video.download()
    except Exception as e:
        print(e)
