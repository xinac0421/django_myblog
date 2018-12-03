from django.shortcuts import render, redirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .utils.extra_views import *
from count_statistics.utils.extra_count import read_statistics_once_read, \
    get_seven_dates_read_sum, get_today_hot_read_data, get_yesterday_hot_read_data
from .models import Article, Tag, User


# 首页视图
class IndexView(generic.ListView):
    template_name = "gregblog/index.html"
    paginate_by = settings.EACH_PAGES_PER  # 分页数设置
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.all().order_by('-id')
        return article_list

    def get_context_data(self, **kwargs):
        # 自定义分页设置
        context_data = super(IndexView, self).get_context_data(**kwargs)
        kwargs['my_page_list'] = paginator_expand(context_data)

        # 自定首页标签数据(利用annotate方法注入注释，可统计每个标签下的文章数，最后过滤掉文章数等于0的标签)
        kwargs['all_tags'] = get_tags_count

        # 自定义首页时间归档数据和排序（按月倒序）
        kwargs['all_dates'] = get_dates_count

        return super(IndexView, self).get_context_data(**kwargs)


# 博客页视图
class BlogView(IndexView):
    template_name = "gregblog/blog.html"

    def get_queryset(self):
        article_list = Article.objects.filter(category__name="博客").order_by('-id')
        return article_list


# 随笔页视图
class MoodView(IndexView):
    template_name = "gregblog/mood.html"

    def get_queryset(self):
        article_list = Article.objects.filter(category__name="随笔").order_by('-id')
        return article_list


# 归档页
class DatesDetailView(IndexView):
    template_name = "gregblog/dates_detail.html"

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        article_list = Article.objects.filter(create_time__year=year, create_time__month=month).order_by('-id')
        return article_list

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        kwargs['year_and_month'] = {'year': year, 'month': month}
        return super(DatesDetailView, self).get_context_data(**kwargs)


# 标签详情页
class TagDetailView(IndexView):
    template_name = "gregblog/tag_detail.html"

    # 标签页里的文章需要筛选为该标签下的数据
    def get_queryset(self):
        tid = self.kwargs.get('pk')
        article_list = Article.objects.filter(tags__pk=tid).order_by('-id')
        return article_list

    # 把当前页的tab数据查询出来后加入模板
    def get_context_data(self, **kwargs):
        kwargs['this_tag'] = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagDetailView, self).get_context_data(**kwargs)


# 文章详情页
class ArticleDetailView(generic.DetailView):
    template_name = "gregblog/article_detail.html"

    def get(self, request, *args, **kwargs):
        aid = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=aid)
        read_cookie_read = read_statistics_once_read(self.request, article)

        # 文章对象放入context上下文中
        context = {'article_detail': article}

        # 博客上一篇与下一篇功能
        context.update(page_turning(Article, aid))
        # 加入标签面板
        context['all_tags'] = get_tags_count
        # 加入日期归档面板
        context['all_dates'] = get_dates_count

        response = self.render_to_response(context)
        response.set_cookie(read_cookie_read, 'true')  # 写入cookie
        return response


# 后台报表，临时存放
def admin_test_page(request):
    article_content_type = ContentType.objects.get_for_model(Article)  # 获取Article模型的ContentType对象(缓存)
    dates, sum_list = cache.get_or_set('seven_dates', get_seven_dates_read_sum(article_content_type), 3600)  # 过去7天的阅读数据(缓存)
    today_read_data = cache.get_or_set('today_read_data', get_today_hot_read_data(article_content_type), 300)  # 当天的阅读数据(缓存)
    yesterday_read_data = cache.get_or_set('yesterday_read_data', get_yesterday_hot_read_data(article_content_type), 3600)  # 昨天的阅读数据(缓存)
    hot_article_for_7day = cache.get_or_set('hot_article_for_7day', get_hot_read_for_days(7), 3600)  # 过去7天的阅读排行(缓存)

    context = {
        'sum_list': sum_list,
        'dates': dates,
        'today_read_data': today_read_data,
        'yesterday_read_data': yesterday_read_data,
        'hot_article_for_7day': hot_article_for_7day
    }
    return render(request, 'gregblog/admin_test.html', context)
