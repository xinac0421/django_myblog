from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from count_statistics.models import ReadDateDetail


# 文章标签
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="标签名称", unique=True)

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章类别
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="类别名称", unique=True)

    class Meta:
        verbose_name = "文章类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    author = models.ForeignKey(User, verbose_name="作者信息", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=64, verbose_name="作者昵称", blank=True)
    title = models.CharField(max_length=200, verbose_name="文章标题")
    content = RichTextUploadingField(verbose_name="文章内容")
    tags = models.ManyToManyField(Tag, verbose_name="文章标签")
    is_myself = models.BooleanField(verbose_name="原创/转载", default=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    comments_num = models.PositiveIntegerField(verbose_name="评论数", default=0)
    is_publish = models.BooleanField(verbose_name="发布状态", default=False)
    thumb_img_url = models.URLField(verbose_name="文章缩略图地址", null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="文章类别", on_delete=models.CASCADE)
    read_date_detail = GenericRelation(ReadDateDetail)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def save(self, *args, **kwargs):
        self.author_name = self.author.last_name + self.author.first_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title





