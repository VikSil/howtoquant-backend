# Generated by Django 4.2.11 on 2024-06-19 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_rename_default_account_id_book_default_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='trade_setlement_xrate',
            new_name='trade_settlement_xrate',
        ),
        migrations.RemoveField(
            model_name='trade',
            name='trade_instrument_xrate',
        ),
    ]
