# Generated by Django 4.0.6 on 2022-08-02 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('kakao_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
