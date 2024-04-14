#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: lixiaobing
Date: 2024/04/14
Desc:
"""

from typing import Any
from xml.sax import ContentHandler
from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.safestring import SafeText

from .models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(
        self, handler: ContentHandler, item: dict[str, Any]
    ) -> None:
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = "Typeidea Blog"
    link = "/rss/"
    description_template = "typeidea is a blog system power by django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item: Model) -> SafeText:
        return item.title

    def item_description(self, item: Model) -> str:
        return item.desc

    def item_link(self, item: Model) -> str:
        return reverse("post-detail", args=[item.pk])
    
    def item_content_html(self, item):
        return item.content_html

    def item_extra_kwargs(self, item: Model) -> dict[Any, Any]:
        return {'content_html': self.item_content_html(item)}
    

