from rest_framework import serializers
from blog.models import Post, Comment
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from blog.api.serializers import PostListSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # post_set = serializers.HyperlinkedRelatedField(many = True, view_name='post-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url','id','username')

class UserDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('url','id','username','posts_count','posts')

    def get_posts(self,obj):
        all_post = Post.objects.filter(author= obj)
        posts = PostListSerializer(all_post,many=True,context=self.context).data
        return posts

    def get_posts_count(self,obj):
        count = obj.post_set.count()
        return count

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id','username','email','password')
    
    def validate_password(self,data):
        return make_password(data)