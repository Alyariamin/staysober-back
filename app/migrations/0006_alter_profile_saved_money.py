# Generated by Django 5.2.4 on 2025-07-13 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_profile_saved_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='saved_money',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6),
        ),
    ]
