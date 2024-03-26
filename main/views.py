from django.shortcuts import render
import feedparser
import re
from bs4 import BeautifulSoup


def sort_by_date(objects):
    sorted_objects = sorted(objects, key=lambda obj: obj['published_parsed'], reverse=True)
    return sorted_objects


def index(request):
    rss_url = "https://techrocks.ru/feed/"
    feed_entries = []
    for i in range(2):
        feed = feedparser.parse(rss_url)
        domain = re.findall('\/\/(.*?)\/', rss_url)[0]

        for entry in feed.entries:
            img = ""
            match = re.search(r'(<img ([^>]+)>)', entry.summary)
            if match:
                img = re.sub(r'<img ([^>]+)>', r'<img width="230" style="margin:auto; display:block" \1>', match[0])
                print(entry.published_parsed)

            summary = BeautifulSoup(entry.summary).get_text().replace("Читать далее", "").replace("Читать дальше", "")[0:250]+"..."
            el = {'icon': 'https://icons.feedercdn.com/' + domain, 'id': entry.id, 'domain': domain, 'title': entry.title, 'img': img, 'description': summary, 'published_parsed': entry.published_parsed, 'published': entry.published}
            feed_entries.append(el)
        rss_url = "https://habr.com/ru/rss/company/postgrespro/blog/?fl=ru"

    feed_entries = sort_by_date(feed_entries)
    data = {"feed_entries": feed_entries}
    return render(request, 'main/home.html', data)
