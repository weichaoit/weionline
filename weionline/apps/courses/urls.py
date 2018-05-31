# _*_ coding: utf-8 _*_
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^course_list/$',CourseListView.as_view(),name='course_list'),
    url(r'^course_detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),
    url(r'^course_info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info'),
    url(r'^course_comment/(?P<course_id>\d+)/$',CourseCommentView.as_view(),name='course_comment'),
    url(r'^add_comment/$',AddCommentView.as_view(),name='add_comment'),
    url(r'^video/(?P<video_id>\d+)/$',VideoPlayView.as_view(),name='video'),
]