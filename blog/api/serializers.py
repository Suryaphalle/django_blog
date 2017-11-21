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

    class Meta:
        model = Comment
        fields = ('post', 'author','parent','text','created_date','approved_comment')

class CommentDetailSerialzer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('post', 'author','text','created_date','approved_comment','replies')

    def get_replies(self,obj):
        replies = CommentSerializer(obj.has_replies(),many=True).data
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
        comments = CommentSerializer(queryset,many=True).data
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