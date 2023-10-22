from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nm_prime = models.CharField(max_length=255)
    nm_usual = models.CharField(max_length=255)


class Ticket(models.Model):
    REGULAR = 'regular'
    PRIME = 'prime'

    TICKET_TYPE_CHOICES = [
        (REGULAR, 'Regular'),
        (PRIME, 'Prime'),
    ]

    event = models.CharField(max_length=255)
    ticket_number = models.CharField(max_length=255, unique=True)
    ticket_holder_name = models.CharField(max_length=255)
    ticket_holder_surname = models.CharField(max_length=255)
    ticket_type = models.CharField(
        max_length=10,
        choices=TICKET_TYPE_CHOICES,
        default=REGULAR,
    )
    date_of_birth = models.CharField(max_length=255, default='2000-01-01')
    price = models.IntegerField(null=True)
    educational_program = models.CharField(max_length=255, null=True)
    educational_course = models.IntegerField(null=True)


class Promouter(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    phone_number = models.BigIntegerField(null=True, default='99999999')

