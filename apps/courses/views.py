# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from .models import Course
from operation.models import UserFavorite

from pure_pagination import Paginator, PageNotAnInteger


class CourseListView(View):
    """
    课程列表页面
    """
    def get(self, request):
        all_courses = Course.objects.all()
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
