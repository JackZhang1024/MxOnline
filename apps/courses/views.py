# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse

from pure_pagination import Paginator, PageNotAnInteger


class CourseListView(View):
    """
    课程列表页面
    """
    def get(self, request):
        all_courses = Course.objects.all()
        search_keywords = request.GET.get("keywords")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))
        hot_courses = all_courses.order_by("-click_nums")[:3]
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by("-click_nums")
            elif sort == 'students':
                all_courses = all_courses.order_by("-students")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
                        "all_courses": courses,
                        "hot_courses": hot_courses,
                        "current_page": sort
        })


class CourseDetailView(View):
    """
    课程详情页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        has_fav_org = False
        has_fav_course = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                has_fav_org = True

            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id), fav_type=1):
                has_fav_course = True

        course.click_nums += 1
        course.save()
        course_tag = course.tag
        if course_tag:
            relate_courses = Course.objects.filter(tag=course.tag)[:1]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_org": has_fav_org,
            "has_fav_course": has_fav_course,
            "relate_courses": relate_courses
        })


class CourseInfoView(View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_resources = CourseResource.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:2]
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses
        })


class CourseVideoPlayView(View):
    """
    课程视频播放
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course_resources = CourseResource.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:2]
        return render(request, "course-video-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video
        })


class CourseCommentsView(View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_resources = CourseResource.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:2]
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses
        })


class AddCommentsView(View):
    """
    添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        course_comment = CourseComments()
        if course_id > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comment.user = request.user
            course_comment.comments = comments
            course_comment.course = course
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "success", "msg": "添加失败"}', content_type='application/json')