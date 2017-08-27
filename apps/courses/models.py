# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u"课程老师", null=True, blank=True)
    name = models.CharField(max_length=150, verbose_name=u"课程名")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否是轮播图")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = UEditorField(verbose_name=u"课程详情", width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/",
                          default='')
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", u'中级'), ("gj", u"高级")), default="cj", max_length=2,
                              verbose_name=u"课程等级")
    learn_times = models.IntegerField(verbose_name=u"学习时长(分钟数)", default=0)
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name=u"课程类别")
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(default=u"", max_length=20, verbose_name=u"课程标签")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    you_need_know = models.CharField(max_length=100, verbose_name=u"课前须知", default=u"")
    what_you_learn = models.CharField(max_length=100, verbose_name=u"知识获取", default=u"")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取课程的章节数目
    def get_lesson_nums(self):
        return self.lesson_set.all().count()
    get_lesson_nums.short_description = u"章节数"

    # 跳转
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com/'>跳转</>")
    go_to.short_description = u"跳转"

    # 获取课程的用户
    def get_course_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程的章节
    def get_lessons(self):
        return self.lesson_set.all()

    # 获取课程评价
    def get_comments(self):
        return self.coursecomments_set.all().order_by('-add_time')[:20]


class BannerCourse(Course):
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(verbose_name=u"章节名", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取章节视频
    def get_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(verbose_name=u"视频名", max_length=100)
    learn_times = models.IntegerField(verbose_name=u"学习时长(分钟数)", default=0)
    video_url = models.CharField(default="", verbose_name=u"视频地址", max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(verbose_name=u"名称", max_length=100)
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
