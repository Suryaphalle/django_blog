from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# post_list = views.PostViewSet.as_view({
#         'get':'list',
#         'post': 'create'
#     })

# post_detail = views.PostViewSet.as_view({
#         'get':'retrive',
#         'put':'update',
#         'patch':'partial_update',
#         'delete':'destroy'

#     })

# user_list = views.UserViewSet.as_view({
#         'get':'list'
#     })

# user_detail = views.UserViewSet.as_view({
#         'get': 'retrive'
#     })

urlpatterns = format_suffix_patterns([

    url(r'^post/$',views.PostListView.as_view(),name='post-list'),
    url(r'^post/create/$',views.PostCreateView.as_view(),name='post-create'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$',views.PostEditView.as_view(),name='post-edit'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$',views.PostDeleteView.as_view(),name='post-delete'),
    url(r'^comment/$', views.CommentListView.as_view() ,name='comment-list'),
    url(r'^comment/create/$',views.CommentCreateView.as_view(),name='comment-create'),
    url(r'^comment/(?P<pk>[0-9]+)/detail/$', views.CommentDetailView.as_view() ,name='comment-detail'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='post-detail'),
    
])