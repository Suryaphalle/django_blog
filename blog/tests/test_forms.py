from django.contrib.auth.models import User
from django.test import TestCase
from blog.forms import PostForm

class PostFormTest(TestCase):
    
    def test_post_form_field(self):
        form = PostForm()
        self.assertTrue(form.fields['title'].label == None or form.fields['title'].label == 'Title')

