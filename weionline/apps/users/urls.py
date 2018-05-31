# _*_ coding: utf-8 _*_
__author__ = 'chaoge'
__date__ = '2018/5/23 9:49'

from django.conf.urls import url
from django.views.generic import TemplateView
from .views import *
urlpatterns = [
    # url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^$',index,name='index'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^active/(?P<code>\w+)/$',ActiveUserView.as_view(),name='active'),
    url(r'^forget/$',ForgetView.as_view(),name='forget_pwd'),
    url(r'^reset/(?P<code>\w+)/$',ResetView.as_view(),name='reset'),
    url(r'^modify_pwd/$',ModifyPwd.as_view(),name='modify_pwd')
]