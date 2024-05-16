import json
import time
from datetime import datetime, timezone


from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import feedparser
import re
from bs4 import BeautifulSoup
from .models import Channels
from .forms import RSSForm
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, Page


def sort_by_date(objects):
    sorted_objects = sorted(objects, key=lambda obj: obj['published_parsed'], reverse=True)
    return sorted_objects


def rss_list(e=None):
    rss = Channels.objects.order_by('-id')
    rss_entries = []
    for entry in rss:
        feed = feedparser.parse(entry.rss_url)
        if "subtitle" in feed.feed:
            description = feed.feed.subtitle
        else:
            description = ""
        domain = re.findall('//(.*?)/', entry.rss_url)[0]
        if e:
            active = str(entry.id) in e
        else:
            active = True
        el = {'icon': 'https://icons.feedercdn.com/' + domain,
              'id': entry.id,
              'active': active,
              'site': domain,
              'title': feed.feed.title,
              'rss_url': entry.rss_url,
              'description': description}
        rss_entries.append(el)
    return rss_entries


def feeds(request):
    feed_entries = return_feed_entries()

    data = {"feeds": feed_entries}
    return HttpResponse(json.dumps(data), content_type='application/json')


def search(request):
    e = request.GET.getlist('e')
    feed_entries = return_feed_entries(e)
    rss_entries = rss_list(e)
    query_e = "&".join(list(map(lambda x: "e=" + x, e)))
    q = request.GET.get('q').lower()
    if q:
        matches = filter(lambda el: el['description'].lower().find(q) != -1 or el['title'].lower().find(q) != -1, feed_entries)
    else:
        matches = feed_entries
    paginator = Paginator(list(matches), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {"feed_entries": page_obj,
            "rss_list": rss_entries,
            "search_params": {"e":query_e,
                              "q":q}}
    return render(request, 'main/home.html', data)


def settings(request):
    rss_entries = rss_list()
    return render(request, 'main/rss_list.html', {"rss": rss_entries})


class RSSFormView(CreateView):
    model = Channels
    template_name = "main/create.html"
    form_class = RSSForm
    success_url = "/settings"


def delete(request, pk):
    data = get_object_or_404(Channels, pk=pk)
    data.delete()
    return redirect('settings')


def return_feed_entries(q=None):
    rss = list(Channels.objects.all())
    if q:
        rss = list(filter(lambda el: str(el.id) in q, rss))
    feed_entries = []
    for rss_entry in rss:
        rss_url = rss_entry.rss_url
        feed = feedparser.parse(rss_url)
        domain = re.findall('//(.*?)/', rss_url)[0]
        for entry in feed.entries:
            if "link" in entry:
                link = entry.link
            else:
                link = entry.id
            if "summary" in entry:
                summary = BeautifulSoup(entry.summary, 'html.parser').get_text().replace("Читать далее", "").replace(
                    "Читать дальше", "")[0:250] + "..."
                img = BeautifulSoup(entry.summary, 'html.parser').img
                if img:
                    img['style'] = "margin:auto; display:block"
                    img['width'] = "230"
                else:
                    img = ""
            else:
                img = ""
                summary = ""
            datetime_obj = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)
            el = {'icon': 'https://icons.feedercdn.com/' + domain,
                  'id': link,
                  'rss_id': str(rss_entry.id),
                  'domain': domain,
                  'title': entry.title,
                  'img': str(img),
                  'description': summary,
                  'published_parsed': entry.published_parsed,
                  'published': datetime_obj}
            if el not in feed_entries:
                feed_entries.append(el)

    return sort_by_date(feed_entries)


def index(request):
    feed_entries = return_feed_entries()
    rss_entries = rss_list()

    paginator = Paginator(feed_entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        "feed_entries": page_obj,
        "rss_list": rss_entries
    }
    return render(request, 'main/home.html', data)