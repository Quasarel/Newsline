from django.db import models


class Channels(models.Model):
    rss_url = models.CharField('RSS', max_length=250)

    def __str__(self):
        return self.rss_url

    class Meta:
        verbose_name = 'Лента'
        verbose_name_plural = 'Ленты'
