# Generated by Django 4.0.6 on 2022-08-05 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_alter_flightroute_departure_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flightroute',
            old_name='airpalne',
            new_name='airplane',
        ),
    ]