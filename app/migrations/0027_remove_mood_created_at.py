# Generated by Django 5.2.4 on 2025-07-19 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_habit_created_at_mood'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mood',
            name='created_at',
        ),
    ]
