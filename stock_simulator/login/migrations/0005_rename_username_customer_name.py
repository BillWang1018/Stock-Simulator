# Generated by Django 4.2.13 on 2024-05-31 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0004_rename_name_customer_username"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="username",
            new_name="name",
        ),
    ]
