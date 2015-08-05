# -*- coding: utf-8 -*-

import hashlib
import re
from datetime import datetime

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.template import RequestContext
from cron_table.models import Cron, CronLine


def index(request):
    html = "<html><body>It is hoge</body></html>"
    return HttpResponse(html)


def create(request):
    """新規作成表示"""
    return render_to_response("edit.html", context_instance=RequestContext(request))


def show(request, cron_hash):

    cron = Cron.objects.get(hash=cron_hash)
    lines = CronLine.objects.filter(cron_id = cron.id)
    return render_to_response("show.html", {"cron": cron, "lines": lines})


def save(request):
    """ 保存処理 """

    # TODO valid 1行以上あること

    cron_text = request.POST['cron_text']
    if len(cron_text) > 16384:
        raise Exception("too big text")

    cron_text_lines = cron_text.splitlines()
    if len(cron_text_lines) > 1000:
        raise Exception("too big text")

    cron = Cron(body = cron_text)
    cron.hash = hashlib.sha256(str(datetime.now())).hexdigest()
    cron.save()

    for i, line_text in enumerate(cron_text_lines):

        line_text = line_text.strip()

        # 空行は飛ばす
        if len(line_text) == 0:
            continue

        # 複数行の空白や、タブは1スペースに置換する
        line_text = re.sub(r'\s{2,}', ' ', line_text)

        if len(line_text) > 1024:
            raise Exception("too big line")

        is_comment = line_text.startswith(u"#")
        is_setting = line_text.count("=") >= 1
        is_cron_line = not is_comment and not is_setting

        # 設定行は飛ばす
        if is_setting:
            continue

        # TODO 分割

        # TODO valid 設定
        # TODO 大きすぎないこと

        # TODO valid

        cron_line = CronLine(cron = cron)
        cron_line.body = line_text
        cron_line.line = i

        if is_cron_line:
            elements = line_text.split(" ")
            if len(elements) < 6:
                continue
            minute = elements[0]
            hour = elements[1]
            day = elements[2]
            month = elements[3]
            week = elements[4]
            command = " ".join(elements[5:])

            # TODO formatチェック
            cron_line.minute = minute
            cron_line.hour = hour
            cron_line.day = day
            cron_line.month = month
            cron_line.week = week
            cron_line.command = command

        cron_line.save()

    return render_to_response("show.html", cron)