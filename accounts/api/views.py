from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, UserDetailSerializer, UserCreateSerializer
from rest_framework import viewsets, generics



class UserView(generics.ListAPIView):
    queryset =User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset =User.objects.all()
    serializer_class = UserDetailSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer