from rest_framework import serializers
from blog.models import Post, Comment

from django.contrib.auth.models import User
from blog.api.serializers import PostListSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # post_set = serializers.HyperlinkedRelatedField(many = True, view_name='post-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url','id','username')

class UserDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('url','id','username','post_set','posts')

    def get_posts(self,obj):
        all_post = Post.objects.filter(author= obj)
        posts = PostListSerializer(all_post,many=True,context=self.context).data
        return posts