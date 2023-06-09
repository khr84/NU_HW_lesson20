# Generated by Django 4.2 on 2023-04-11 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hh_search_app', '0005_alter_vacancy_salary_from_alter_vacancy_salary_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='vacancy_url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterUniqueTogether(
            name='vacancy',
            unique_together={('search_id', 'vacancy_url')},
        ),
    ]
