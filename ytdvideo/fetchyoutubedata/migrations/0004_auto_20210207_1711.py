# Generated by Django 2.2.3 on 2021-02-07 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetchyoutubedata', '0003_auto_20210207_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideoapikey',
            name='status',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'InActive')], db_index=True, default=0, max_length=50),
        ),
    ]
