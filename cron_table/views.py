# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.template import RequestContext
from cron_table.models import Cron


def index(request):
    html = "<html><body>It is hoge</body></html>"
    return HttpResponse(html)

def create(request):
    """新規作成表示"""
    return render_to_response("edit.html", context_instance=RequestContext(request))

def save(request):
    """ 保存 """

    # validation

    cron = Cron(body = request.POST['cron_text'])
    cron.hash = hashlib.sha256(str(datetime.now())).hexdigest()
    cron.save()

    # TODO CronLine

    return render_to_response("show.html", cron)