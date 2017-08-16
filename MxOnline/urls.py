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
# from django.views.generic import TemplateView
import xadmin
from django.views.static import serve


# from users.views import user_login
from users.views import IndexView, LoginView, RegisterView, ActivateUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, LogoutView
# from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT, STATIC_ROOT


urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),

    # TemplateView.as_view(tempalate_name='index.html') 适用于处理静态页面
    # url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),

    # url(r'^login/$', TemplateView.as_view(template_name="login.html"), name='login'),  # template_name 必不可少
    # url(r'^login/$', user_login, name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),

    url(r'^logout/$', LogoutView.as_view(), name='logout'),
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
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 配置静态文件static的访问处理函数
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 用户Url配置
    url(r'^user/', include('users.urls', namespace="user"))

]

# 全局404页面 (Page Not Found 通常是没有配置该页面或者方法)
handler404 = 'users.views.page_not_fount'
# 全局500页面 (Internal Server Error 通常是程序出错显示)
handler500 = 'users.views.page_server_error'



