# Generated by Django 4.2.6 on 2023-10-15 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("nm_prime", models.CharField(max_length=255)),
                ("nm_usual", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Promouter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField(unique=True)),
                ("username", models.CharField(max_length=255)),
                ("full_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ticket_number", models.CharField(max_length=255, unique=True)),
                ("ticket_holder_name", models.CharField(max_length=255)),
                ("ticket_holder_surname", models.CharField(max_length=255)),
                ("ticket_type", models.CharField(max_length=255)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.event"
                    ),
                ),
            ],
        ),
    ]