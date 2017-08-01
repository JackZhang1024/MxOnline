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
@time: 2017/8/1 13:42
"""
from django.conf.urls import url


from .views import UserInfoView, UserCoursesView, UserFavCoursesView, UserMessagesView, UserFavOrgsView, UserFavTeachersView
from .views import UploadImageView, UpdateUserPwdView


urlpatterns = [
    # 课程机构首页
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户课程
    url(r'^courses/$', UserCoursesView.as_view(), name='user_courses'),
    # 用户课程收藏
    url(r'^favs/courses/$', UserFavCoursesView.as_view(), name='user_fav_courses'),
    # 用户收藏机构
    url(r'^favs/orgs/$', UserFavOrgsView.as_view(), name='user_fav_orgs'),
    # 用户收藏教师
    url(r'^favs/teachers/$', UserFavTeachersView.as_view(), name='user_fav_teachers'),
    # 用户消息
    url(r'^messages/$', UserMessagesView.as_view(), name='user_messages'),
    # 用户头像上传
    url(r'^upload/image/$', UploadImageView.as_view(), name='upload_image'),
    # 修改用户中心密码
    url(r'^update/pwd/$', UpdateUserPwdView.as_view(), name='update_userpwd')
]