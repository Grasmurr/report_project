from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nm_prime = models.CharField(max_length=255)
    nm_usual = models.CharField(max_length=255)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=255, unique=True)
    ticket_holder_name = models.CharField(max_length=255)
    ticket_holder_surname = models.CharField(max_length=255)
    ticket_type = models.CharField(max_length=255)


class Promouter(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)

