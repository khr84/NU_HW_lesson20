# Generated by Django 4.2 on 2023-04-11 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hh_search_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='search_vacancy',
            unique_together={('search_str', 'region_id')},
        ),
    ]
