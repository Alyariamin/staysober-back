# Generated by Django 5.2.4 on 2025-07-15 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_journal_triggers_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='completed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
