#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: lixiaobing
Date: 2024/04/14
Desc:
"""

from django.contrib.sitemaps import Sitemap
from django.db.models.base import Model
from django.urls import reverse

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)
    
    def lastmod(self, obj):
        return obj.created_time
    
    def location(self, obj: Model) -> str:
        return reverse('post-detail', args=[obj.pk])
