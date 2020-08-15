from datetime import datetime

import feedparser
import json
import schedule
import time
from google.cloud import datastore
from newsplease import NewsPlease
from tldextract import tldextract

visiteds = {}

def set_visited(url):
    visiteds[url] = True


def is_visited(url):
    res = False
    if url in visiteds:
        res = True

    return res


def parse_all():
    targets = json.load(open("rss.json"))
    try:
        datastore_client = datastore.Client()
    except:
        print("Datastore client exception")


    for t in targets:
        try:
            feed = feedparser.parse( t["url"] )
        except:
            print("feedparser", t["url"])
            continue

        for entry in feed["entries"]:
            try:

                url = entry.link
                if is_visited(url):
                    continue
                # print(entry.link, entry.title, entry.published_parsed, entry.summary)
                # The kind for the new entity
                kind = 'News_Entry'
                # The name/ID for the new entity
                # The Cloud Datastore key for the new entity
                task_key = datastore_client.key(kind, url)

                published = time.strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed) if entry.published_parsed is not None else time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed)

                article = parse_article(url)

                # Prepares the new entity
                task = datastore.Entity(key=task_key, exclude_from_indexes=["description", "text", "np_description"])
                task.update({
                    "link": url,
                    "title": entry.title,
                    "published": published,
                    "description": entry.summary,
                    "np_published": article.date_publish,
                    "np_title": article.title,
                    "np_description": article.description,
                    "source_domain": article.source_domain,
                    "parsed_at": str(datetime.now()),
                    "text": article.text
                })

                set_visited(url)

                # Saves the entity
                datastore_client.put(task)
            except:
                print(entry.__dict__)
                print(entry)
                print(json.dumps(entry))


def parse_article(url):

    article = NewsPlease.from_url(url)

    return article

schedule.every(15).minutes.do(parse_all)

while True:
    schedule.run_pending()
    time.sleep(1)