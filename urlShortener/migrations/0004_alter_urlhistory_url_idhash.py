# Generated by Django 3.2.8 on 2021-10-31 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlShortener', '0003_remove_urlhistory_url_createddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlhistory',
            name='url_IdHash',
            field=models.CharField(default='', max_length=8),
        ),
    ]
