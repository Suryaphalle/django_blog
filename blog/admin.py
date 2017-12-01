# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from accounts.models import Profile
from blog.models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','views','approved','created_date','updated_date')
    list_display_links = ('title', 'author')
    list_filter = ('author', 'updated_date')

admin.site.register(Post,PostAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','email_confirmed','acitvated','timestamp')

admin.site.register(Profile,ProfileAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','author','created_date','parent')
    list_filter = ('post', 'author')

admin.site.register(Comment,CommentAdmin)
admin.site.empty_value_display = '(None)'