from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import (UserSerializer, UserDetailSerializer, UserCreateSerializer, SignUpSerializer, LoginSerializer)
from rest_framework import viewsets, generics
from permissions import IsAuthenticatedOrCreate, IsSuperUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class UserView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'accounts/user_list.html'

    def get(self, request):
        queryset =User.objects.all()
        serializer = UserSerializer(queryset)
        return Response({'users': queryset, 'serializer': serializer })

class UserDetailView(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'accounts/user_detail.html'
    # serializer_class = UserDetailSerializer

    def get(self, request, pk):
        user_detail = get_object_or_404(User, pk=pk)
        serializer = UserDetailSerializer(user_detail, many=True)
        return Response({'user_detail': user_detail, 'serializer': serializer})  

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,IsSuperUser)


@api_view(['POST'])
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
        # login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token":token.key}, status=HTTP_200_OK)
        else:
            return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)