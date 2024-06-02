# Generated by Django 5.0.6 on 2024-06-02 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='inventory',
            fields=[
                ('cid', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('num', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('price', models.FloatField(max_length=50)),
                ('stmp', models.TimeField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='quotations',
            fields=[
                ('snum', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('Buyamt', models.IntegerField()),
                ('sellamt', models.IntegerField()),
                ('tstmp', models.TimeField(max_length=50, unique=True)),
                ('sprice', models.FloatField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='stock',
            fields=[
                ('sname', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('overamt', models.IntegerField()),
            ],
        ),
    ]
