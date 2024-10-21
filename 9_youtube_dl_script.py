# NOT CLEANED YET AS OF 21 OCT 2024
# BUT UPLOADED AS THIS WILL HAPPEN SOON (and uploading creates pressure to do so!)


from __future__ import unicode_literals
import youtube_dl
import pandas as pd
import json

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': '136', #135
    #'playlist_items': '1-10',
    'outtmpl': '~/Videos/%(id)s',
    #'ignoreerrors': True,
    #'writeinfojson': True,
    'sleep_interval': 15,
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'wav',
    #     'preferredquality': '192',
    # }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

filename = 'data/cctv_videos.csv'
filename_have = './data/done_cctv_videos.jsonl'
df = pd.read_csv(filename)
#df2 = pd.read_csv(filename_have)
data_df = pd.read_json(filename_have, lines=True)

column =  'url'
urls = list(df[column])#[63:] # slice here, len jsonl -1

already_have = list(data_df[column])

fetch = [url for url in urls if url not in already_have]

print(len(fetch))

for url in fetch:
    print(url)
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        save_done = {"url": url}
        with open ('./data/done_cctv_videos.jsonl', 'a') as f:
            json.dump(save_done, f)
            f.write('\n')
    except:
        print('Error with: ' + url)
        save_done = {"url": url}
        with open ('./data/error_cctv_videos.jsonl', 'a') as f:
            json.dump(save_done, f)
            f.write('\n')      
        pass

'''
# For CCTV direct
format code  extension  resolution note
http         mp4        unknown    
hls-460      mp4        480x270     460k 
hls-870      mp4        640x360     870k 
hls-1228     mp4        1280x720   1228k  (best)

'''