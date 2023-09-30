import datetime

from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, related_name='consultas', on_delete=models.CASCADE)
    data_consulta = models.DateTimeField(default=timezone.now)
    texto_convertido = models.TextField()