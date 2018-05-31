# _*_ coding: utf-8 _*_
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^org_list/$',OrgView.as_view(),name='org_list'),
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teacher'),
    url(r'^add_fav/$',AddFavView.as_view(),name='add_fav')
]