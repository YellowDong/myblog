#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from .models import Post


class AllRssPostsFeed(Feed):
    title = '小云柳的博客更新啦！！！'
    link = 'all/rss'
    description = '博客更新的具体文章'

    def item(self):
        return Post.objects.all()

    def item_title(self, item):
        return f'{item.category}, {item.title}'

    def item_description(self, item):
        return item.body