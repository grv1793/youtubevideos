# Generated by Django 2.2.3 on 2021-02-07 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videothumbnail',
            old_name='field_name',
            new_name='url',
        ),
        migrations.AddField(
            model_name='videothumbnail',
            name='type',
            field=models.CharField(choices=[('default', 'DEFAULT TYPE'), ('medium', 'MEDIUM TYPE'), ('high', 'HIGH TYPE')], db_index=True, default='default', max_length=50),
            preserve_default=False,
        ),
    ]
