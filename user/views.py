import random
import string
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import LoginForm, RegisterForm, ChangeNicknameForm, \
    ChangeEmailForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile


# 登录
def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']  # user验证已在forms里的clean方法验证
            login(request, user)
            return redirect(request.GET.get('from', reverse('gregblog:index')))
    else:
        if not request.user.is_authenticated:
            login_form = LoginForm()
        else:
            return redirect(request.GET.get('from', reverse('gregblog:index')))

    context = {'login_form': login_form}

    return render(request, 'user/login.html', context)


# 注册
def register_view(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            # 创建用户
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # 注册成功后自动登录
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('gregblog:index')))
    else:
        if not request.user.is_authenticated:
            register_form = RegisterForm()
        else:
            return redirect(request.GET.get('from', reverse('gregblog:index')))

    context = {'register_form': register_form}
    return render(request, 'user/register.html', context)


# 退出登录
def logout(request):
    auth.logout(request)  # 退出登录
    return redirect(request.GET.get('from', reverse('gregblog:index')))


# 用户信息
def user_info(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'user/user_info.html', context)
    else:
        return redirect(request.GET.get('from', reverse('gregblog:index')))


# 修改昵称
def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('gregblog:index'))
    if request.method == 'POST':
        change_nickname_form = ChangeNicknameForm(request.POST, user=request.user)
        if change_nickname_form.is_valid():
            new_nickname = change_nickname_form.cleaned_data['nickname_new']

            # 修改昵称
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = new_nickname
            profile.save()

            return redirect(redirect_to)
    else:
        if request.user.is_authenticated:
            change_nickname_form = ChangeNicknameForm()
        else:
            return redirect(redirect_to)

    context = dict()
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = change_nickname_form
    context['return_back_url'] = redirect_to

    return render(request, 'public/form.html', context)


# 修改邮箱
def change_email(request):
    redirect_to = request.GET.get('from', reverse('gregblog:index'))
    if request.method == 'POST':
        change_email_form = ChangeEmailForm(request.POST, user=request.user)
        if change_email_form.is_valid():
            email_new = change_email_form.cleaned_data['email_new']

            # 修改邮箱
            user = request.user
            user.email = email_new
            user.save()

            return redirect(redirect_to)
    else:
        if request.user.is_authenticated:
            change_email_form = ChangeEmailForm()
        else:
            return redirect(redirect_to)

    context = dict()
    context['page_title'] = '修改邮箱'
    context['form_title'] = '修改邮箱'
    context['submit_text'] = '修改'
    context['form'] = change_email_form
    context['return_back_url'] = redirect_to

    return render(request, 'public/form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('gregblog:index'))
    if request.method == 'POST':
        bind_email_form = BindEmailForm(request.POST, request=request)
        if bind_email_form.is_valid():
            profile, create = Profile.objects.get_or_create(user=request.user)
            profile.email_is_active = True
            profile.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        if request.user.is_authenticated:
            bind_email_form = BindEmailForm(request=request)
        else:
            return redirect(redirect_to)

    context = dict()
    context['page_title'] = '邮箱认证'
    context['form_title'] = '邮箱认证'
    context['submit_text'] = '认证'
    context['form'] = bind_email_form
    context['return_back_url'] = redirect_to

    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')  # 验证码的类别区分：邮箱认证、密码找回等
    data = dict()
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_uppercase + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
            data['message'] = '验证码获取太频繁，请稍后再试'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now

            # 编辑邮件内容
            context = {
                'text': '您的验证码为：%s, 请及时使用' % code
            }
            html_text = render_to_string('public/send_email.html', context)

            # 发送邮件
            send_mail(
                '[王不迟的博客]邮箱认证',  # 邮件主题
                '',     # 邮件纯文本内容
                settings.EMAIL_HOST_USER,  # 发件人
                [email],  # 收件人
                fail_silently=False,
                html_message=html_text  # 邮件html内容
            )
            data['status'] = 'SUCCESS'
            data['message'] = '邮件发送成功，请及时查看您的邮箱'
    else:
        data['status'] = 'ERROR'
        data['message'] = '验证码不能为空'
    return JsonResponse(data)


def change_password(request):
    redirect_to = request.GET.get('from', reverse('gregblog:index'))
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST, user=request.user)
        if change_password_form.is_valid():
            new_password = change_password_form.cleaned_data['new_password']

            # 修改密码
            user = request.user
            user.set_password(new_password)  # set_password方法可加密
            user.save()

            return redirect(redirect_to)
    else:
        if request.user.is_authenticated:
            change_password_form = ChangePasswordForm()
        else:
            return redirect(redirect_to)

    context = dict()
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = change_password_form
    context['return_back_url'] = redirect_to

    return render(request, 'public/form.html', context)


def forgot_password(request):
    redirect_to = reverse('user:login')
    if request.method == 'POST':
        forgot_password_form = ForgotPasswordForm(request.POST, request=request)
        if forgot_password_form.is_valid():
            email = forgot_password_form.cleaned_data.get('email', '')
            new_password = forgot_password_form.cleaned_data['new_password']
            print('email', email)
            user = User.objects.get(email=email)
            # 修改密码
            user.set_password(new_password)
            user.save()
            # 同时若邮箱没有认证过的，则自动认证
            profile, create = Profile.objects.get_or_create(user=user)
            if profile.email_is_active is False:
                profile.email_is_active = True
                profile.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        forgot_password_form = ForgotPasswordForm()

    context = dict()
    context['page_title'] = '密码找回'
    context['form_title'] = '密码找回'
    context['submit_text'] = '修改密码'
    context['form'] = forgot_password_form
    context['return_back_url'] = redirect_to

    return render(request, 'user/forgot_password.html', context)
