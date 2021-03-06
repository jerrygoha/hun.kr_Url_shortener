# Generated by Django 3.2.8 on 2021-10-31 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrlHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_originalAddr', models.URLField(max_length=300)),
                ('url_encodedAddr', models.URLField(default='')),
                ('url_createdDate', models.DateTimeField(auto_now_add=True)),
                ('url_visitedCount', models.IntegerField(default=0)),
            ],
        ),
    ]
