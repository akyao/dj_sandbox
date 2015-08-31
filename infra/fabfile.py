# -*- coding: utf-8 -*-

from fabric.api import run, local, lcd, env, hosts, cd, prompt, put,sudo
from datetime import date,datetime
from fabric.colors import *

env.use_ssh_config = True

VENV_PATH="/var/venv/env27"

def deploy():
    # tmpディレクトリに移動。git clone
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    work_dir = "/tmp/{0}".format(now)
    local("mkdir {0}".format(work_dir))
    with lcd(work_dir):
        local("git clone --depth 1 git@github.com:akyao/dj_sandbox.git")
        with lcd("dj_sandbox"):
            # 余計なファイルを削除
            local("rm -rf .git .idea .gitignore")
            # infraとか消す？
            # 設定ファイルなどの内容を本番用に置き換える
            local("touch prod.txt")
        # サーバーにアップロード
        local("mv dj_sandbox dj_sandbox{0}".format(now))
        put("dj_sandbox{0}".format(now), "work")

    local("rm -rf {0}".format(work_dir))

    # サーバー作業
    sudo("mv work/dj_sandbox{0} /var/www/html".format(now))
    sudo("rm -f /var/www/html/dj_sandbox")
    sudo("ln -s /var/www/html/dj_sandbox{0} /var/www/html/dj_sandbox".format(now))

    sudo("/etc/init.d/httpd restart")

    # TODO google analytics

def mig():
    """migrate"""
    with cd("/var/www/html/dj_sandbox"):
        run("source {0}/bin/activate && python manage.py migrate".format(VENV_PATH))
