# Generated by Django 5.0.6 on 2024-05-28 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('identity', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('account', models.CharField(max_length=30, unique=True)),
                ('ctfc', models.CharField(max_length=30, unique=True)),
            ],
        ),
    ]
