# —*- coding:utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve


# from users.views import user_login
from users.views import LoginView, RegisterView, ActivateUserView, ForgetPwdView, ResetPwdView, ModifyPwdView
# from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    # url(r'^login/$', TemplateView.as_view(template_name="login.html"), name='login'),  # template_name 必不可少
    # url(r'^login/$', user_login, name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^activate/(?P<active_code>.*)/$', ActivateUserView.as_view(), name='activate'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构Url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    # 机构课程Url配置
    url(r'^course/', include('courses.urls', namespace="course")),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})

]
