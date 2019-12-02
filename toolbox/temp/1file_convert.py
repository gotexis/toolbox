import os
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

FILE = os.path.join(BASE_DIR, 'dave-AS6MAxN4-20190131.mp3')
OUT_FILE = f'{FILE}.wav'
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')


album = 'EQ'
artist = "蔡康永"
bitrate = "192k"
output_format = "wav"


AudioSegment.from_file(FILE).export(
    OUT_FILE,
    format=output_format,
    bitrate=bitrate,
    tags={"album": album, "artist": artist},
)

