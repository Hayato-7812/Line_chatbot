import ssl
from pytube import YouTube
ssl._create_default_https_context = ssl._create_unverified_context

def get_yt_info(url):
    print("get YouTube link info (URL: '{}')".format(url))
    yt = YouTube(url)
    ret = dict (title=yt.title,thumbnail_url=yt.thumbnail_url)
    print(ret)
    return ret

if __name__ =="__main__":
    get_yt_info('https://www.youtube.com/watch?v=ME-jTVzjXME')