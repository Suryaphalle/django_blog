from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import status, mixins, generics, permissions, viewsets, renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from blog.models import Post
from .serializers import PostSerializer, UserSerializer
from .permissions import IsAutherReadOnly

@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'user': reverse('user-list', request= request, format=format),
        'post': reverse('post-list', request=request, format=format)
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset =User.objects.all()
    serializer_class = UserSerializer


# class UserList(generics.ListAPIView):
#     queryset =User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#     queryset =User.objects.all()
#     serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)

    # @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(author= self.request.user)
    
# class PostList(generics.ListCreateAPIView):
    
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)

#     def perform_create(self, serializer):
#         serializer.save(author= self.request.user)
    
# class PostDetail(generics.RetrieveUpdateDestroyAPIView):

#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAutherReadOnly)
    


# @api_view(['GET', 'POST'])
# def post_list(request):

#     if request.method == 'GET':
#         post= Post.objects.all()
#         serializer = PostSerializer(post,many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors,status=400)

# @api_view(['GET', 'POST','DELETE'])
# def post_detail(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
