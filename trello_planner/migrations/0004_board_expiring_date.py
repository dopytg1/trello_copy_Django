# Generated by Django 4.1.3 on 2022-12-16 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello_planner', '0003_remove_checklist_is_checked_checklistelement'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='expiring_date',
            field=models.DateTimeField(null=True),
        ),
    ]
