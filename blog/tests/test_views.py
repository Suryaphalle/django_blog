from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Post
from django.core.urlresolvers import reverse

class PostListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test1',email='test@gmail.com',password='ts123123')
        user = User.objects.first()
        num_of_post = 13
        for post in range(num_of_post):
            Post.objects.create(author=user,
                                title='Post no %s' % post, 
                                text='This text of post no %s' % post
                                )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/blog/')
        self.assertEqual(resp.status_code,200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('post_list'))
        self.assertEqual(resp.status_code,200)
    
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('post_list'))
        self.assertEqual(resp.status_code,200)
        self.assertTemplateUsed(resp,'blog/post_list.html')   

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('post_list'))
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertEqual(len(resp.context['posts']), 3)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('post_new'))
        self.assertEqual(resp.status_code,302)
        self.assertTrue(resp.url.startswith('/login/?next=/blog/post/new/'))

    def test_redirect_if_login(self):
        login = self.client.login(username='test1',password='ts123123')
        self.assertTrue(login)
        resp = self.client.get(reverse('post_list'))

        self.assertEqual(resp.status_code,200)

    # def test_form_invalid(self):
    #     login = self.client.login(username='test1',password='ts123123')
    #     