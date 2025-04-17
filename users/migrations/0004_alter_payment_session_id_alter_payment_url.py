# Generated by Django 5.2 on 2025-04-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_payment_session_id_payment_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="session_id",
            field=models.CharField(
                blank=True, max_length=55, null=True, verbose_name="session id"
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="url",
            field=models.CharField(
                blank=True, max_length=55, null=True, verbose_name="url"
            ),
        ),
    ]
