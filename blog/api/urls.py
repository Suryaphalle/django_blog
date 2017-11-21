from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostViewSet, UserViewSet, api_root

# post_list = PostViewSet.as_view({
#         'get':'list',
#         'post': 'create'
#     })

# post_detail = PostViewSet.as_view({
#         'get':'retrive',
#         'put':'update',
#         'patch':'partial_update',
#         'delete':'destroy'

#     })

# user_list = UserViewSet.as_view({
#         'get':'list'
#     })

# user_detail = UserViewSet.as_view({
#         'get': 'retrive'
#     })

# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^post/$',post_list,name='post-list'),
#     url(r'^post/(?P<pk>[0-9]+)/$', post_detail , name='post-detail'),
#     url(r'^users/$', user_list ,name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$', user_detail , name='user-detail'),    
# ])