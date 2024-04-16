# Generated by Django 4.2.5 on 2024-03-30 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("staticdata", "0002_organization_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="owner_org_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="staticdata.organization",
            ),
        ),
    ]