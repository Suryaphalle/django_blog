from django.conf.urls import url, include
from . import views



urlpatterns = [

    # url(r'^$', views.post_list, name='post_list'),
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>\d+)/detail/$', views.PostDetailView.as_view(), name='post_detail'),
    # url(r'^like/$',views.post_like, name='like'),
    url(r'^post/(?P<pk>\d+)/edit/$',views.PostUpdateView.as_view(),name='post_edit'),
    url(r'^post/(?P<pk>\d+)/del/$',views.PostDeleteView.as_view(),name='del_blog'),
    # url(r'^post/search_post/$', views.BlogSearchListView.as_view(), name='search_post'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/new/$', views.PostCreateView.as_view(), name='post_new'),
    # url(r'^post/(?P<pk>\d+)/detail/$',views.post_detail, name='post_detail'),
    # url(r'^post/(?P<pk>\d+)/edit/$',views.post_edit,name='post_edit'),
    # url(r'^post/(?P<pk>\d+)/del/$',views.del_blog,name='del_blog'),
    url(r'^password/$', views.change_password, name='change_password'),
    # url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post_title/$',views.search_post_title, name = 'post_title'),  
]