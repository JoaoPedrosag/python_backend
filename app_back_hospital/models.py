import datetime

from django.db import models
from django.utils import timezone


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Consult(models.Model):
    patient = models.ForeignKey(Patient, related_name='records', on_delete=models.CASCADE)
    consultation_date = models.DateTimeField(default=timezone.now)
    converted_text = models.TextField()
