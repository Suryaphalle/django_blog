from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, UserDetailSerializer
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'user': reverse('user-list', request= request, format=format)
        })

class UserView(generics.ListAPIView):
    queryset =User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset =User.objects.all()
    serializer_class = UserDetailSerializer