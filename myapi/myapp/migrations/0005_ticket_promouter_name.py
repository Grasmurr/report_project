# Generated by Django 4.2.6 on 2023-11-24 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_alter_ticket_ticket_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="promouter_name",
            field=models.CharField(max_length=255, null=True),
        ),
    ]