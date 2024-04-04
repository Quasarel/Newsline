from django.shortcuts import render, redirect, get_object_or_404
import feedparser
import re
from bs4 import BeautifulSoup
from .models import Channels
from .forms import RSSForm
from django.views.generic.edit import CreateView


def sort_by_date(objects):
    sorted_objects = sorted(objects, key=lambda obj: obj['published_parsed'], reverse=True)
    return sorted_objects


def settings(request):
    rss = Channels.objects.order_by('-id')
    rss_entries = []
    for entry in rss:
        feed = feedparser.parse(entry.rss_url)
        domain = re.findall('//(.*?)/', entry.rss_url)[0]
        el = {'icon': 'https://icons.feedercdn.com/' + domain,
              'id': entry.id,
              'site': domain,
              'title': feed.feed.title,
              'rss_url': entry.rss_url,
              'description': feed.feed.subtitle}
        rss_entries.append(el)
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


def index(request):
    rss = Channels.objects.order_by('-id')
    feed_entries = []
    for rss_entry in rss:
        rss_url = rss_entry.rss_url
        feed = feedparser.parse(rss_url)
        domain = re.findall('//(.*?)/', rss_url)[0]
        for entry in feed.entries:
            img = BeautifulSoup(entry.summary, 'html.parser').img
            if img:
                img['style'] = "margin:auto; display:block"
                img['width'] = "230"
            else:
                img = ""
            summary = BeautifulSoup(entry.summary, 'html.parser').get_text().replace("Читать далее", "").replace(
                "Читать дальше", "")[0:250] + "..."
            el = {'icon': 'https://icons.feedercdn.com/' + domain,
                  'id': entry.id,
                  'domain': domain,
                  'title': entry.title,
                  'img': str(img),
                  'description': summary,
                  'published_parsed': entry.published_parsed,
                  'published': entry.published}
            if el not in feed_entries:
                feed_entries.append(el)

    feed_entries = sort_by_date(feed_entries)
    data = {"feed_entries": feed_entries}
    return render(request, 'main/home.html', data)
