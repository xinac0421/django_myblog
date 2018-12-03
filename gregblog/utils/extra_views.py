from datetime import timedelta
from django.db.models import Count, Sum
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from gregblog.models import Article, Tag, User


def paginator_expand(context_data):
    """
    自定义分页扩展
    :param context_data: 通用模板里的context
    :return:
    """
    gap_number = settings.PAGES_GAP_NUMBER  # 设置显示当前页前后显示间距
    page_obj = context_data.get('page_obj')
    paginator = context_data.get('paginator')
    if page_obj and paginator:
        currentr_page_num = page_obj.number  # 当前页
        my_page_list = [x for x in range(currentr_page_num - gap_number, currentr_page_num + gap_number + 1) if
                        x in paginator.page_range]

        # 加上省略号标记
        if currentr_page_num - gap_number > 2:
            my_page_list.insert(0, '...')
        if currentr_page_num + gap_number + 1 < paginator.num_pages:
            my_page_list.append('...')
        # 加上首页和尾页
        if my_page_list[0] != 1:
            my_page_list.insert(0, 1)
        if my_page_list[-1] != paginator.num_pages:
            my_page_list.append(paginator.num_pages)
        return my_page_list
    else:
        return {
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
        }


def page_turning(model, oid):
    """
    翻页功能
    :param model: 模块名
    :param oid: 当前页对象的id
    :return: 返回翻页需要的数据字典（是否有上一页下一页，上一页下一页数据的对象）
    """
    # 上一篇与下一篇
    has_prev = False
    has_next = False
    context = {}
    article_next = model.objects.filter(id__gt=oid).first()  # 查找id大于当前文章的文章
    article_prev = model.objects.filter(id__lt=oid).first()  # 查找id小于当前文章的文章
    if article_next:
        has_next = True
        context.update({'article_next': article_next})
    if article_prev:
        has_prev = True
        context.update({'article_prev': article_prev})
    context.update({'has_next': has_next, 'has_prev': has_prev})
    return context


def get_tags_count():
    """
    标签面板数据模块：利用annotate方法注入注释，可统计每个标签下的文章数，最后过滤掉文章数等于0的标签
    :return: 返回标签对象和计数
    """
    return Tag.objects.annotate(num_tags=Count('article')).filter(num_tags__gt=0)


def get_dates_count():
    """
    日期归档面板数据模块
    :return: 返回日期归档对象和计数
    """
    all_dates = Article.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for date in all_dates:
        num_dates = Article.objects.filter(create_time__year=date.year, create_time__month=date.month).count()
        blog_dates_dict[date] = num_dates
    return blog_dates_dict


def get_hot_read_for_days(days):
    """
    得到days天的文章阅读量排行
    days: 天数
    :return: 返回days天的文章阅读量排行
    """
    today = timezone.now().date()
    to_days = today - timedelta(days=days)
    aritlce_list = Article.objects\
        .filter(read_date_detail__date__lt=today, read_date_detail__date__gte=to_days)\
        .values('id', 'title')\
        .annotate(read_num_sum=Sum('read_date_detail__read_num'))\
        .order_by('-read_num_sum')
    return aritlce_list[:5]






