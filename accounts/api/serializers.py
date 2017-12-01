from rest_framework import serializers
from blog.models import Post, Comment
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from blog.api.serializers import PostListSerializer
from rest_framework.authtoken.models import Token

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
        fields = ('url','id','username','posts_count','published_date','posts')

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

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')

class LoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
                'username',
                'password',
                'token',
        ]
        extra_kwargs = {"password":
        {"write_only": True}
        }

    def validate(self, data):
        username = data['username']
        qs = User.objects.filter(username=username) 
        if qs.exists():
            user = qs.first()
            email = user.email
            token, _ = Token.objects.get_or_create(user=user)
            data = {
            'username':username,
            'token':token,
            'email':email,
            }
        return data