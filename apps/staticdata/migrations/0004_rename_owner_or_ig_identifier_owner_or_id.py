# Generated by Django 4.2.5 on 2024-03-30 23:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("staticdata", "0003_alter_organization_owner_org_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="identifier",
            old_name="owner_or_ig",
            new_name="owner_or_id",
        ),
    ]
