# Generated by Django 4.1.3 on 2022-12-14 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello_planner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='column_id',
        ),
        migrations.AddField(
            model_name='column',
            name='cards_inside',
            field=models.ManyToManyField(to='trello_planner.card'),
        ),
    ]
