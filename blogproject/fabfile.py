#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "https://github.com/YellowDong/myblog.git"
env.user = "dong"
env.password = "dongdong"
env.hosts = ["xiaoyunliu.pro"]
env.port = "22"


def deploy():
    source_path = "/home/dong/sites/demo.xiaoyunliu.pro/myblog/blogproject"
    run('cd %s && git pull' % source_path)
    run("""
        cd {} &&
        pipenv install --dev &&
        pipenv run python manage.py collectstatic --noinput &&
        pipenv run python manage.py makemigrations &&
        pipenv run python manage.py migrate
        """.format(source_path))
    sudo("restart gunicorn-demo.xiaoyunliu.pro")
    sudo("service nginx reload")
