from .models import Channels
from django.forms import ModelForm, TextInput, ValidationError
import re


class RSSForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        rss_url = cleaned_data.get("rss_url")

        if re.findall('//(.*?)/', rss_url):
            if Channels.objects.filter(rss_url=rss_url):
                raise ValidationError("Такой RSS уже используется")
            else:
                return cleaned_data
        else:
            raise ValidationError("Адрес ленты должен соответствовать URL страницы на сайте с XML-данными RSS-канала")

    class Meta:
        model = Channels
        fields = ['rss_url']

        widgets = {
            "rss_url": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес ленты'
            })
        }
