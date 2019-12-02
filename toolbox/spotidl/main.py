import subprocess
import os

# set proxy
proxy = "http://127.0.0.1:1080"
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


album_url = "https://open.spotify.com/album/44M7t659RJPdbnxNWhDf7M"


txt_file = subprocess.run(["spotdl", "--album", album_url], capture_output=True)

txt_file = txt_file.stderr.decode().rstrip()

txt_file = txt_file.split("to ")[1]

txt_basename = os.path.basename(txt_file)

album_name = txt_basename.replace(".txt", "")


subprocess.run(["spotdl", f"--list={txt_file}", "-f", f"E:/user/Music/spotify/{album_name}/"])

