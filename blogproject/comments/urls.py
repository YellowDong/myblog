#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path(r'comment/post/<int:pk>', views.post_comment, name='post_comment')
]
