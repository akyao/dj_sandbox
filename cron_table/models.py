# -*- coding: utf-8 -*-

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

    def __unicode__(self):
        return self.body

    def calc_hours(self):
        import re
        h = re.sub(r'\s', '', self.hour)

        if self.hour == "*":
            return range(0, 60)

        hours = []
        for he in h.split(","):

            dash = he.count("-") > 0
            slash = he.count("/") > 0

            if dash and not slash:
                # 2-14
                h_from, h_to = he.split("-")
                hours.extend(range(int(h_from), int(h_to) + 1))
            elif not dash and slash:
                # TODO */n とみなしてよい？
                n = int(he.split("/")[1])
                hours.extend(range(0, 60 , n))
            elif dash and slash:
                # 2-59/5
                front, back = he.split("/")
                front_from, front_to = front.split("-")
                hours.extend(range(int(front_from), int(front_to), int(back)))
            else:
                hours.append(int(he))

        return sorted(list(set(hours)))