from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    
    url(r'^users/$', views.UserView.as_view(), name='user-list'),
    url(r'^users/create/$', views.UserCreateView.as_view(), name='user-create'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^users/sign-up/$', views.SignUpView.as_view(), name='sign-up'),
    url(r'^login/$',views.LoginAPIView.as_view(), name='login')
    # url(r'^social_sign_up/$', views.SocialSignUp.as_view(), name="social_sign_up"),
])