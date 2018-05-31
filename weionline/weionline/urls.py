"""weionline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
from django.views.static import serve
from .settings import MEDIA_ROOT

import xadmin


urlpatterns = [
    path('admin/', xadmin.site.urls),
    # 用户信息url配置
    url(r'^',include('users.urls')),
    url(r'captcha/',include('captcha.urls')),
    # 课程机构url配置
    url(r'^org/',include('organization.urls')),
    # 课程相关url配置
    url(r'^course/',include('courses.urls')),
    # 配置上传文件访问url
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
    # 配置ueditor
    url(r'ueditor/',include('extra_apps.DjangoUeditor.urls'))
]
