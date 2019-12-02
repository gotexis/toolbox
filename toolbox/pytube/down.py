from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=xPEbvBxc4xo&list=PLWoqVaAYKDsw7BYg4CgyQpK_W7WqyZ-cA')
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
