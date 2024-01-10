# Generated by Django 4.2.6 on 2023-11-23 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_ticket_ticket_holder_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="ticket_type",
            field=models.CharField(
                choices=[
                    ("regular", "Regular"),
                    ("prime", "Prime"),
                    ("deposit", "deposit"),
                ],
                default="regular",
                max_length=20,
            ),
        ),
    ]