import os
from multiprocessing import Pool
from pydub import AudioSegment

def worker(filename):
  song = AudioSegment.from_wav(filename)
  song.export(filename.replace(".wav",".flac"), format = "flac")

if __name__ == '__main__':
  converted_count = 0
  convertlist = []
  for filename in os.listdir(os.getcwd()):
    if filename.endswith(".wav"):
      convertlist.append(filename)
      converted_count += 1
  p = Pool(processes=min(converted_count, os.cpu_count()))
  p.map(worker, convertlist)