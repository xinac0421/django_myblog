from datetime import timedelta
from django.db.models import Count, F, Sum
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from count_statistics.models import ReadNum, ReadDateDetail


def read_statistics_once_read(request, obj):
    """
    阅读数限制：按cookies是否失效限制，cookies不存在则阅读总数+1，天数+1
    :param request:
    :param obj:
    :return:
    """
    ct = ContentType.objects.get_for_model(obj)
    cookie = '%s_%s_have_read' % (ct.model, obj.pk)

    if not request.COOKIES.get(cookie):
        # 简单计数
        obj_readnum, created = ReadNum.objects.get_or_create(
            content_type=ct,
            object_id=obj.pk,
            defaults={'read_num': 0}
        )
        obj_readnum.read_num = F('read_num') + 1
        obj_readnum.save()

        # 按天计数
        obj_readnum, created = ReadDateDetail.objects.get_or_create(
            content_type=ct,
            object_id=obj.pk,
            date=timezone.now(),
            defaults={'read_num': 0}
        )
        obj_readnum.read_num = F('read_num') + 1
        obj_readnum.save()

    return cookie


def get_seven_dates_read_sum(content_type):
    """
    获取过去7天的阅读数列表
    :param content_type: 模型的ContentType对象
    :return:返回过去7天的日期(月/日)和阅读数列表
    """
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - timedelta(days=i)
        dates.append("%s/%s" % (date.month, date.day))
        read_date = ReadDateDetail.objects.filter(content_type=content_type, date=date)
        read_date_sum = read_date.aggregate(read_date_sum=Sum('read_num'))  # 聚合查询，计数阅读数之和
        read_nums.append(read_date_sum['read_date_sum'] or 0)
    return dates, read_nums


def get_today_hot_read_data(content_type):
    """
    当天的阅读量排行(前5条)
    :param content_type: 模型的ContentType对象
    :return: 返回排序好的阅读数据
    """
    today = timezone.now().date()
    today_read_date = ReadDateDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return today_read_date[:5]


def get_yesterday_hot_read_data(content_type):
    """
    昨天的阅读量排行(前5条)
    :param content_type: 模型的ContentType对象
    :return: 返回排序好的阅读数据
    """
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    yesterday_read_date = ReadDateDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return yesterday_read_date[:5]
