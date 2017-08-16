# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import sys

from django.db import models
from django.contrib.auth.models import AbstractUser


reload(sys)
sys.setdefaultencoding("utf-8")

# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(choices=(("male", u"男"), ("female", u"女")), max_length=6, default="female", verbose_name=u"性别")
    address = models.CharField(max_length=100, default="", verbose_name=u"地址")
    mobile = models.CharField(max_length=11, default="", verbose_name=u"手机", null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100, verbose_name=u"头像")

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def unread_message_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=(
                                         ('register', u"注册"),
                                         ('forgot',   u'忘记密码'),
                                         ('update_email',   u'修改邮箱')
                                         ),
                                 max_length=12, verbose_name=u"验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.email


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u"轮播图", max_length=100)  # 存储在mysql中路径地址
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title




