from django.db import models
from django.contrib.postgres.fields import ArrayField


class Event(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ticket_number_start = models.IntegerField(null=False, default=100)
    nm_prime = models.IntegerField(null=False)
    nm_usual = models.IntegerField(null=False)
    nm_deposit = models.IntegerField(null=False, default=0)
    date_of_event = models.DateField(default='2023-11-11')
    prices = ArrayField(models.IntegerField(), null=True)
    is_hidden = models.BooleanField(default=False)


class Ticket(models.Model):
    REGULAR = 'regular'
    PRIME = 'prime'
    DEPOSIT = 'deposit'

    TICKET_TYPE_CHOICES = [
        (REGULAR, 'Regular'),
        (PRIME, 'Prime'),
        (DEPOSIT, 'deposit'),
    ]

    event = models.CharField(max_length=255)
    ticket_number = models.IntegerField()
    ticket_holder_name = models.CharField(max_length=255)
    ticket_holder_surname = models.CharField(max_length=255)
    ticket_holder_sex = models.CharField(null=True)
    ticket_type = models.CharField(
        max_length=20,
        choices=TICKET_TYPE_CHOICES,
        default=REGULAR,
    )
    date_of_birth = models.CharField(max_length=255, default='2000-01-01')
    price = models.IntegerField(null=True)
    educational_program = models.CharField(max_length=255, null=True)
    educational_course = models.IntegerField(null=True)
    phone_number = models.BigIntegerField(null=True, default='99999999')
    is_refunded = models.BooleanField(default=False)
    promouter_name = models.CharField(max_length=255, null=True)


class Promouter(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    phone_number = models.BigIntegerField(null=True, default='99999999')

