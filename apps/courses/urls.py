#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
@version: ??
@author: zfz
@license: Apache Licence
@contact: zhangfengzhou@aragoncs.com
@site: http://github.com/zhangfengzhou
@software: PyCharm
@file: urls.py
@time: 2017/7/18 16:25
"""

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentsView, AddCommentsView, CourseVideoPlayView

urlpatterns = [
        url(r'^list/$', CourseListView.as_view(), name='course_list'),
        url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
        url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
        url(r'^comments/(?P<course_id>\d+)/$', CourseCommentsView.as_view(), name='course_comments'),
        url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comment'),
        url(r'^video/(?P<video_id>\d+)/$', CourseVideoPlayView.as_view(), name='course_video'),
]
