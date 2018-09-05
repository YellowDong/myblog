#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fabric.api import env, run, cd
from fabric.operations import sudo

GIT_REPO = 'https://github.com/YellowDong/myblog.git'
env.user = 'dong'
env.password = 'dongdong'
env.hosts = ['xiaoyunliu.pro']
env.port = '22'


def deploy():
    source_path = '/home/dong/sites/demo.xiaoyunliu.pro/myblog/blogproject'
    with cd('{}'.format(source_path)):

        run('git pull')
        run("""
            pipenv install &&
            pipenv run python manage.py collectstatic --noinput &&
            pipenv run python manage.py makemigrations &&
            pipenv run python manage.py migrate
            """)
    sudo('restart gunicorn-demo.xiaoyunliu.pro')
    sudo('service nginx reload')
