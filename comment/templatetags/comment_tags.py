from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


# 自定义模板标签：获取评论数
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


# 自定义模板标签：评论表单
@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 加入评论Form
    comment_form = CommentForm(initial={'content_type': content_type.model,
                                        'object_id': obj.pk,
                                        'reply_comment_id': 0})
    return comment_form


# 自定义模板标签：获取评论列表
@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_list = Comment.objects.filter(content_type=content_type,
                                          object_id=obj.pk,
                                          root=None)
    return comment_list.order_by('-comment_time')




