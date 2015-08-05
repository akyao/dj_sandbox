from django.db import models

class Cron(models.Model):
    body = models.CharField(max_length=16384)
    hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CronLine(models.Model):
    class Meta:
        db_table = "cron_table_cron_line"
    cron = models.ForeignKey(Cron)
    line = models.IntegerField()
    body = models.CharField(max_length=1024, null=True)
    command = models.CharField(max_length=1024, null=True)
    month = models.CharField(max_length=1024, null=True)
    day = models.CharField(max_length=1024, null=True)
    week = models.CharField(max_length=1024, null=True)
    hour = models.CharField(max_length=1024, null=True)
    minute = models.CharField(max_length=1024, null=True)