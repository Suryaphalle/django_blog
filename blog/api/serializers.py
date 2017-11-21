from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    post_set = serializers.HyperlinkedRelatedField(many = True, view_name='post-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url','id','username','post_set')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields =('url','author','title','text','views','created_date','published_date','updated_date')