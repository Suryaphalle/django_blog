# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Post

# Create your tests here.
class PostModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test1',email='test@gmail.com',password='ts123123')
        user = User.objects.first()
        Post.objects.create(
            author=user,
            title='Test Post',
            text='This is Test Post'
            )

    def test_first_title_label(self):
        user = Post.objects.get(id=1)
        field_label = user._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title') 

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length,200)

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(),'/blog/post/1/detail/')
