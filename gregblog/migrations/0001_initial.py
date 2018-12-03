# Generated by Django 2.1.3 on 2018-11-12 20:48

import ckeditor_uploader.fields
import count_statistics.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(blank=True, max_length=64, verbose_name='作者昵称')),
                ('title', models.CharField(max_length=200, verbose_name='文章标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='文章内容')),
                ('is_myself', models.BooleanField(default=True, verbose_name='原创/转载')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('comments_num', models.PositiveIntegerField(default=0, verbose_name='评论数')),
                ('is_publish', models.BooleanField(default=False, verbose_name='发布状态')),
                ('thumb_img_url', models.URLField(blank=True, null=True, verbose_name='文章缩略图地址')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者信息')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-create_time'],
            },
            bases=(models.Model, count_statistics.models.CountNumExpandMethod),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户账号')),
                ('password', models.CharField(max_length=128, verbose_name='登录密码')),
                ('nickname', models.CharField(blank=True, max_length=64, null=True, verbose_name='昵称')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='手机号码')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('avatar_img_url', models.URLField(blank=True, null=True, verbose_name='个人头像图片地址')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否注销')),
                ('login_count', models.PositiveIntegerField(default=0, verbose_name='登录次数')),
                ('update_time', models.DateTimeField(blank=True, null=True, verbose_name='最近一次登录时间')),
                ('note', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='类别名称')),
            ],
            options={
                'verbose_name': '文章类别',
                'verbose_name_plural': '文章类别',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('from_user', models.CharField(max_length=100, verbose_name='评论者名字')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gregblog.Article', verbose_name='文章')),
            ],
            options={
                'verbose_name': '博客评论',
                'verbose_name_plural': '博客评论',
            },
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='回复内容')),
                ('from_id', models.PositiveIntegerField(verbose_name='回复用户id')),
                ('to_id', models.PositiveIntegerField(verbose_name='目标用户id')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gregblog.Comment', verbose_name='评论关联')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='标签名称')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='gregblog.Category', verbose_name='文章类别'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='gregblog.Tag', verbose_name='文章标签'),
        ),
    ]
