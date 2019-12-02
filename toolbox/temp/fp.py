import os
import glob

path = 'F:/郭论'

files = os.listdir(path)[1:]

for filename in files:
    title, ext = os.path.splitext(os.path.basename(filename))
    old_path_and_file = os.path.join(path, filename)
    new_title = title[22:].replace('（', '').replace('）', '')
    new_title_with_ext = new_title + ext
    new_title_with_path = os.path.join(path, new_title_with_ext)
    os.rename(old_path_and_file,
              new_title_with_path)
