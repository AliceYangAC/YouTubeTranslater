from pytubefix import YouTube

try:
    yt = YouTube("https://www.youtube.com/watch?v=sqcess88xCo")
    print(yt.title)
except Exception as e:
    print("Error:", e)
