import feedparser
import time
import database
import requests

def create(rss):
    for post in rss.entries:
        if base.check_post_by_url(post.link)==True:
            continue
        base.add_post(rss.feed.title.replace('\'', '\'\''), post.published, post.title.replace('\'', '\'\''), post.summary.replace('\'', '\'\''), post.link)

base = database.Database()

def run():
    while True:
        for stream in base.get_rss():
            rss=feedparser.parse(stream[0])
            create(rss)
        #print('WAIT')
        time.sleep(interval)

interval=300
run()
