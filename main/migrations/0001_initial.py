# Generated by Django 5.0.3 on 2024-04-03 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rss_url', models.CharField(max_length=250, verbose_name='RSS')),
            ],
            options={
                'verbose_name': 'Лента',
                'verbose_name_plural': 'Ленты',
            },
        ),
    ]
