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

from .views import CourseListView, CourseDetailView

urlpatterns = [
        url(r'^list/$', CourseListView.as_view(), name='course_list'),
        url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail')
]
