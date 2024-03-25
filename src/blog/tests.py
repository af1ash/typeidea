#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: lixiaobing
Date: 2024/03/25
Desc:
"""

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Category

# Create your tests here.

class SimpleTest(TestCase):

    def setUp(self):
        test_user = User.objects.create(
            first_name='tester'
        )
        test_category = Category.objects.create(
            name='test_catgory',
            owner=test_user
        )
        Post.objects.create(
            title="post1",
            desc="test post",
            content="test post content",
            category=test_category,
            owner=test_user
        )

    def test_get_post_data(self):
        """ Post data """
        lion = Post.objects.get(title="post1")
        self.assertEqual(lion.desc, 'test post')

    def test_admin(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)

    def test_super_admin(self):
        response = self.client.get("/super_admin")
        self.assertEqual(response.status_code, 301)

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        response = self.client.get("/post/1.html")
        self.assertEqual(response.status_code, 200)
