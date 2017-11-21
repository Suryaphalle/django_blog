from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.contrib.auth.models import User
import datetime

from rest_framework import status, mixins, generics, permissions, viewsets, renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from blog.models import Post, Comment
from .serializers import (PostSerializer, UserSerializer, PostListSerializer, 
                            PostDetailSerializer, CommentSerializer, CommentDetailSerialzer, 
                            PostCreateSerializer, PostEditSerializer, PostDeleteSerializer,
                            CommentCreateSerializer)
from .permissions import IsAutherReadOnly

@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'user': reverse('user-list', request= request, format=format),
        'post': reverse('post-list', request=request, format=format),
        'comment': reverse('comment-list', request=request, format=format)
    })

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)

    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(author= self.request.user)    

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)

class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerialzer
    permissions_class = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)

class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)

    def perform_create(self, serializer):
        serializer.save(author= self.request.user)
        serializer.save(published_date= datetime.datetime.now())

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    Permission_classes = (permissions.AllowAny,)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    Permission_classes = (permissions.AllowAny,)

class PostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author= self.request.user)
        serializer.save(published_date= datetime.datetime.now())

class PostEditView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostEditSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_edit(self, serializer):
        serializer.save(author= self.request.user)
        serializer.save(published_date= datetime.datetime.now())

class PostDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDeleteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)