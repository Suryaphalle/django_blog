"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from blog import views
from accounts import views as accounts_views
from django.views.generic import TemplateView
from tastypie.api import Api
from blog.api.views import PostViewSet, UserViewSet, api_root
from rest_framework.routers import DefaultRouter

# from blog.api import AjaxSearchResource

# rest_api = Api(api_name='v1')
# rest_api.register(AjaxSearchResource())

router = DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    url(r'^login/$',auth_views.login,name='login'),
    url(r'^logout/$',auth_views.logout,name='logout'),
    # url(r'^signup/$',views.signup, name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/',include('blog.urls')),
    url(r'^profiles/',include('accounts.urls',namespace='profiles')),
    # url(r'^api/',include(rest_api.urls)),
    # url(r'^api/',include('blog.api.urls')),
    url(r'^accounts/',include('allauth.urls')),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(),name='about_us'),
    url(r'^posts-api/', include(router.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls',namespace='pages')),
    url(r'^contact/$', views.ContactView.as_view(),name='contact'),
    url(r'^signup/$',accounts_views.signup, name='signup'),
    url(r'^ajax/validate_username/$',accounts_views.validate_username, name='validate_username'),
    url(r'^profile/$',accounts_views.MyProfileView.as_view(),name='my_profile'),
    url(r'^reset/$',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ),
    name='password_reset'),
    url(r'^reset/done/$',
    auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
    name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
    name='password_reset_confirm'),
    url(r'^reset/complete/$',
    auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    name='password_reset_complete'),

    url(r'^account_activation_sent/$', accounts_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        accounts_views.activate, name='activate'),


]

urlpatterns += [
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]