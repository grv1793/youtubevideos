# Generated by Django 2.2.3 on 2021-02-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210207_0800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videothumbnail',
            name='video',
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnails',
            field=models.ManyToManyField(default=None, related_name='videos', to='api.VideoThumbnail'),
        ),
    ]
