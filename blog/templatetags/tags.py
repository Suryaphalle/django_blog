from django import template
from ..models import Post
from django.db.models import Q, Count
register = template.Library()

@register.inclusion_tag('blog/includes/custom_tags.html')
def most_viewed_posts():
    post_list = Post.objects.all().order_by('-views')[:5]
    return {'post_list': post_list }

@register.inclusion_tag('blog/includes/custom_tags.html')
def latest_added_posts():
    post_list = Post.objects.all().order_by('-updated_date')[:5]
    return {'post_list': post_list }

@register.inclusion_tag('blog/includes/custom_tags.html')
def most_commented_posts():
    posts_objects = Post.objects.annotate(num_comments=Count('comments'))
    post_list = posts_objects.order_by('-num_comments')[:5]
    return {'post_list': post_list }