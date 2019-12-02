import os
import glob
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# input settings
INPUT_DIR = BASE_DIR
extension_list = ('*.mp4', '*.webm')

# output settings
OUTPUT_DIR = os.path.join(INPUT_DIR, 'output')
album = 'EQ'
artist = "蔡康永"
bitrate = "192k"

# what is already converted
present_files = os.listdir(OUTPUT_DIR)
present_titles = [os.path.splitext(f)[0] for f in os.listdir(OUTPUT_DIR)]

# os.chdir(BASE_DIR)
for extension in extension_list:
    videos = glob.glob(os.path.join(INPUT_DIR, extension))
    for video in videos:
        title = os.path.splitext(os.path.basename(video))[0]

        if title in present_titles:
            print(f"SKIP - {title}")
            continue

        outfile = f'{title}.mp3'
        file_with_path = os.path.join(OUTPUT_DIR, outfile)
        AudioSegment.from_file(video).export(file_with_path,
                                             format='mp3',
                                             bitrate=bitrate,
                                             tags={"album": album, "artist": artist},)
        print(f"DONE - {title}.")

