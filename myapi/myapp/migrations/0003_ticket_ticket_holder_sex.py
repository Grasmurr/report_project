# Generated by Django 4.2.6 on 2023-11-05 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_event_nm_deposit"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="ticket_holder_sex",
            field=models.CharField(null=True),
        ),
    ]