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

urlpatterns = [
    url(r'^login/$',auth_views.login,name='login'),
    url(r'^logout/$',auth_views.logout,name='logout'),
    # url(r'^signup/$',views.signup, name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/',include('blog.urls')),
    url(r'^accounts/',include('accounts.urls',namespace='accounts')),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^about/$', views.AboutView.as_view(),name='about_us'),
    url(r'^contact/$', views.ContactView.as_view(),name='contact'),
    url(r'^signup/$',views.SignUpView.as_view(), name='signup'),
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

]
