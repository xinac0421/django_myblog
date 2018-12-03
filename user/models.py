from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 扩展用户信息
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    email_is_active = models.BooleanField(default=False, verbose_name='邮箱认证')

    class Meta:
        verbose_name = "用户扩展信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)


# 获取昵称，如果没有则返回空
def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


# 判断昵称是否存在
def has_nickname(self):
    if Profile.objects.filter(user=self).exists():
        return True
    else:
        return False


# 获取昵称，如果没有昵称则返回用户名
def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


# 获取邮箱是否认证状态
def get_email_active(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.email_is_active
    else:
        return False


# 动态绑定
User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username
User.get_email_active = get_email_active

