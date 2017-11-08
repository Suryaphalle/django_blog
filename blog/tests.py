# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Post
# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test1',email='test@gmail.com',password='ts123123')
        user = User.objects.first()
        Post.objects.create(
            author=user,
            title='Test Post',
            text='This is Test Post'
            )

    def test_post(self):
        post = Post.objects.get(title = 'Test Post')
        # self.assertEqual(post.text(),'This is Test Post')
        self.assertEqual(post.title,'Test Post')