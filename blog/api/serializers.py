from rest_framework import serializers
from blog.models import Post, Comment

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

class CommentSerializer(serializers.ModelSerializer):
    replies_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id','url','post','author','username','parent','text','created_date','replies_count')

    def get_replies_count(self,obj):
        replies_count = obj.has_replies().count()
        return replies_count

    def get_username(self,obj):
        return obj.author.username

class CommentDetailSerialzer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id','post','author','text','created_date','replies')

    def get_replies(self,obj):
        replies = CommentSerializer(obj.has_replies(),many=True,context=self.context).data
        return replies

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields= ('post','author','text')

class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields=('url','title','author','text','views','comment_count','created_date','published_date','comments')

    def get_comments(self,obj):
        queryset = Comment.objects.filter(post=obj)
        comments = CommentSerializer(queryset,many=True,context=self.context).data
        return comments

    def get_comment_count(self,obj):
        count = obj.comments.count()
        return count

class PostListSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields=('url','title','author','text','views','comment_count','created_date','published_date')

    def get_comment_count(self,obj):
        count = obj.get_comment.count()
        return count

class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('title','text')


class PostEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title','text')


class PostDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title','text')