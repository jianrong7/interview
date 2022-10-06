from pymongo import MongoClient
import feedparser
from time import strftime
import os
import datetime
from bs4 import BeautifulSoup


def get_content():
    content_dict = {}
    directory = os.fsencode("./html")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        p = "./html/" + filename
        with open(p, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            mydivs = soup.find_all("div", {"class": "article-body"})
            if len(mydivs) == 1:
                content_dict[filename] = mydivs[0].get_text()
            else:
                content_dict[filename] = ""

    return content_dict


def parse_rss(content_dict):
    docs = []

    feed = feedparser.parse("./rss/521283d13a9b3e3c27b690b6")

    for entry in feed["entries"]:
        d = strftime("%Y-%m-%dT%H:%M:%SZ", entry["published_parsed"])
        iso = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ")
        docs.append(
            {
                "guid": entry["id"],
                "link": entry["links"][0]["href"],
                "title": entry["title"],
                "description": entry["description"],
                "pubdate": iso,
                "category": entry["tags"][0]["term"],
                "content": content_dict[entry["id"]],
            }
        )
    return docs


def main():
    content_dict = get_content()
    docs = parse_rss(content_dict)

    # USERNAME and PASSWORD hidden for security reasons
    uri = "mongodb+srv://USERNAME:PASSWORD@cluster0.lxaoa.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)

    db = client.interview
    coll = db.article

    result = coll.insert_many(docs)

    client.close()


main()
"""
terminal command to export mongodb data to json

mongoexport --uri mongodb+srv://USERNAME:PASSWORD@cluster0.lxaoa.mongodb.net/interview
--collection article --type json --out out.json --pretty --jsonArray
"""
