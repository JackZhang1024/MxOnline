# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from .models import Course
from operation.models import UserFavorite


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
        return render(request, "course-list.html", {
                        "all_courses": all_courses,
                        "hot_courses": hot_courses,
                        "current_page": sort
        })


class CourseDetailView(View):
    """
    课程详情页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_org = course.course_org
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, "course-detail.html", {"course": course, "has_fav": has_fav})
