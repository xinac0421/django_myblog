from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ReadNum


register = template.Library()


# 自定义模板标签：获取阅读数
@register.simple_tag
def get_read_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
    return readnum.read_num







