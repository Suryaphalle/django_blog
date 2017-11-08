from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from .managers import PostManager

class Post(models.Model):
    author = models.ForeignKey('auth.user')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    views = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField( default =timezone.now)
    published_date = models.DateTimeField( blank=True, null=True)
    updated_date = models.DateTimeField( default =timezone.now)

    objects = PostManager()

    class Meta:
        ordering = ['-published_date']


    def publish():
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    @property
    def get_comment(self):
        instance = self
        qs = Comment.objects.filter(post=instance)
        return qs


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey('auth.user')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='replies')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)


    class Meta:
        ordering = ['-created_date']

    def approve(self):
        self.approved_comment = True
        self.save()

    def has_replies(self):
        return Comment.objects.filter(parent=self)

    def __str__(self):
        return self.text
