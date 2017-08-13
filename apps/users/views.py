# -*- coding:utf-8 -*-
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print e.message
            return None


class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm()
        if modifypwd_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if password1 != password2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user_profile = UserProfile.objects.get(email=email)
            user_profile.password = make_password(password1)
            user_profile.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modifypwd_form": modifypwd_form})


class ResetPwdView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "activate_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email=email, send_type="forgot")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})


class ActivateUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "activate_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            password = request.POST.get("password", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()
            send_register_email(email=user_profile.email, send_type="register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户名未激活 "})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误 "})
        else:
            return render(request, "login.html", {"login_form": login_form})


# Create your views here.
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html", {})
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误 "})
    elif request.method == "GET":
        return render(request, "login.html", {})


# 用户信息
class UserInfoView(LoginRequiredMixin, View):
    """
    用户信息
    """
    def get(self, request):
        return render(request, "usercenter-info.html", {})


# 用户课程
class UserCoursesView(View):
    def get(self, request):
        return render(request, "usercenter-mycourse.html", {})


# 用户课程收藏
class UserFavCoursesView(View):
    def get(self, request):
        return render(request, "usercenter-fav-course.html", {})


# 用户机构收藏
class UserFavOrgsView(View):
    def get(self, request):
        return render(request, "usercenter-fav-org.html", {})


# 用户教师收藏
class UserFavTeachersView(View):
    def get(self, request):
        return render(request, "usercenter-fav-teacher.html", {})


# 用户消息
class UserMessagesView(View):
    def get(self, request):
        return render(request, "usercenter-message.html", {})


# 用户头像上传处理
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        # 第一种写法
        # image_form = UploadImageForm(request.POST, request.FILES)
        # if image_form.is_valid():
        #     #  image = image_form.cleaned_data['image']
        #     #  request.user.image = image
        #     # request.user.save()

        # 第二种写法
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdateUserPwdView(View):
    """
    修改用户中心密码
    """
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return HttpResponse('{"status": "fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(password1)
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modifypwd_form.errors), content_type='application/json')
