import feedparser
import time
import database
import requests

DEBUG = True
api = 'https://api.nikitonsky.tk/'
if DEBUG:
    api = 'http://127.0.0.1:55556/'

def create(rss):
    for post in rss.entries:
        if base.check_post_by_url(post.link)==True:
            continue
        r = requests.post(api+'add_post', data = {'src':rss.feed.title.replace('\'', '\'\''), 'date':post.published, 'title':post.title.replace('\'', '\'\''), 'short':post.title.replace('\'', '\'\''), 'url':post.link})

base = database.Database()

def run():
    while True:
        for stream in base.get_rss_url():
            rss=feedparser.parse(stream[0])
            create(rss)
        print('WAIT')
        time.sleep(interval)

interval=300
run()
