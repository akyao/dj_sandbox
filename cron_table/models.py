from django.db import models

class Cron(models.Model):
    body = models.CharField(max_length=16384)
    hash = models.CharField(max_length=64)

class CronLine(models.Model):
    body = models.CharField(max_length=1024)
    command = models.CharField(max_length=1024)
    month = models.CharField(max_length=1024)
    day = models.CharField(max_length=1024)
    week = models.CharField(max_length=1024)
    hour = models.CharField(max_length=1024)
    minute = models.CharField(max_length=1024)