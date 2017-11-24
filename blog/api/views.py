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
from django.db.models import Q
from blog.models import Post, Comment
from .serializers import (PostSerializer, UserSerializer, PostListSerializer, 
                            PostDetailSerializer, CommentSerializer, CommentDetailSerialzer, 
                            PostCreateSerializer, PostEditSerializer, PostDeleteSerializer,
                            CommentCreateSerializer )
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
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        try:
           post_id =self.kwargs['post_id']
           if post_id is not None:
                queryset = Comment.objects.filter(
                   Q(parent=None),
                   Q(post=post_id)
                   )
                return queryset
        except:
            pass
        return queryset
 
class CommentRepliesListAPIView(generics.ListAPIView):
   serializer_class = CommentSerializer
 
   def get_queryset(self):
       queryset = Comment.objects.filter(parent!=None)
       return queryset

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
    model = Post
    serializer_class = PostListSerializer
    Permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.query_params.get('q',None)
        if query is not None:
            queryset = Post.objects.search(query)
        return queryset

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