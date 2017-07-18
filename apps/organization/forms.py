#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
@version: ??
@author: zfz
@license: Apache Licence
@contact: zhangfengzhou@aragoncs.com
@site: http://github.com/zhangfengzhou
@software: PyCharm
@file: forms.py
@time: 2017/7/16 22:50
"""
from django import forms
from operation.models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = "^1[3|4|5|8][0-9]\d{4,8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
