# Generated by Django 4.2.5 on 2024-05-20 02:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book",
            old_name="default_account_id",
            new_name="default_account",
        ),
    ]
