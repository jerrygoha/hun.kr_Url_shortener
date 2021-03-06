# Generated by Django 3.2.8 on 2021-10-31 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlShortener', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlhistory',
            name='url_encodedAddr',
        ),
        migrations.RemoveField(
            model_name='urlhistory',
            name='url_visitedCount',
        ),
        migrations.AddField(
            model_name='urlhistory',
            name='url_IdHash',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='urlhistory',
            name='url_UrlHash',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='urlhistory',
            name='url_originalAddr',
            field=models.URLField(max_length=500),
        ),
    ]
