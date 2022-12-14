# Generated by Django 4.1.3 on 2022-12-15 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trello_planner', '0002_remove_card_column_id_column_cards_inside'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='is_checked',
        ),
        migrations.CreateModel(
            name='CheckListElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('is_checked', models.BooleanField(default=False)),
                ('cheklist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trello_planner.checklist')),
            ],
        ),
    ]
