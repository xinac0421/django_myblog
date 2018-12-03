from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="用户名或邮箱", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名或邮箱',
    }))

    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入密码',
    }))

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email', '')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                email_user = User.objects.get(email=username_or_email)
                # 邮箱是否认证
                if Profile.objects.filter(user=email_user).exists() and Profile.objects.get(user=email_user).email_is_active:
                    user = authenticate(username=email_user.username, password=password)
                    if user is not None:
                        self.cleaned_data['user'] = user
                        return self.cleaned_data
                else:
                    raise forms.ValidationError('您的邮箱还没有认证，认证通过后方可通过邮箱登录')

            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名",
                               max_length=20,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'})
                               )

    email = forms.EmailField(label="邮箱",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
                             )

    password = forms.CharField(label="密码",
                               min_length=6,
                               max_length=15,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
                               )
    password_again = forms.CharField(label="再次输入密码",
                                     min_length=6,
                                     max_length=15,
                                     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'})
                                     )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已注册')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        else:
            return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        else:
            return password_again


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='新的昵称',
                                   max_length=20,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control',
                                              'placeholder': '请输入新的昵称',
                                              }
                                   ))

    def __init__(self, *args, **kwargs):
        # 获取views中实例化时传入的user参数，使用完需删除不影响父类
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('您还未登录,请先登录后再操作')

        # 内容不能为空
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('昵称不能为空')

        return self.cleaned_data


class ChangeEmailForm(forms.Form):
    email_new = forms.EmailField(
        label='新的邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的邮箱'})
    )

    def __init__(self, *args, **kwargs):
        # 获取views中实例化时传入的user参数，使用完需删除不影响父类
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('您还未登录,请先登录后再操作')

        # 内容不能为空
        email_new = self.cleaned_data.get('email_new', '').strip()
        if email_new == '':
            raise forms.ValidationError('邮箱不能为空')
        else:
            self.cleaned_data['email_new'] = email_new

        return self.cleaned_data


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        disabled=True,
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        # 获取views中实例化时传入的request参数，使用完需删除不影响父类
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        # 更新表单里的默认值
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'value': self.request.user.email
        })

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('您还未登录,请先登录后再操作')

        return self.cleaned_data

    def clean_email(self):
        email = self.request.user.email
        if Profile.objects.filter(user=self.request.user).exists() and Profile.objects.get(user=self.request.user).email_is_active:
            raise forms.ValidationError('您已认证过邮箱，不能重复认证')
        return email

    def clean_verification_code(self):
        user_input_code = self.cleaned_data.get('verification_code', '').strip()
        code = self.request.session.get('bind_email_code', '')
        if user_input_code == '':
            raise forms.ValidationError('验证码不能为空')
        elif code != user_input_code:
            raise forms.ValidationError('验证码不正确')
        return user_input_code


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="旧的密码",
        min_length=6,
        max_length=15,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入旧的密码'}
        )
    )

    new_password = forms.CharField(
        label="新的密码",
        min_length=6,
        max_length=15,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}
        )
    )

    new_password_again = forms.CharField(
        label="请再次输入新密码",
        min_length=6,
        max_length=15,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        # 获取views中实例化时传入的user参数，使用完需删除不影响父类
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('您还未登录,请先登录后再操作')

        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password != new_password_again or new_password.strip() == '':
            raise forms.ValidationError({'new_password_again': '两次输入的密码不一致'})
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(label="您的邮箱", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入您绑定的邮箱',
    }))

    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击"发送验证码"发送到邮箱'}
        )
    )

    new_password = forms.CharField(
        label="新的密码",
        min_length=6,
        max_length=15,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入新的密码',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        # 获取views中实例化时传入的request参数，使用完需删除不影响父类
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email  # 单独验证里不能返回self.cleaned_data,不然会把cleaned_data里的字典赋值给email返回

    def clean_verification_code(self):
        user_input_code = self.cleaned_data.get('verification_code', '').strip()
        code = self.request.session.get('forgot_password_code', '')
        if user_input_code == '':
            raise forms.ValidationError('验证码不能为空')
        elif code != user_input_code:
            raise forms.ValidationError('验证码不正确')
        return user_input_code
