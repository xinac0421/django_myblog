from django.urls import path, re_path

from . import views

app_name = 'gregblog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('mood/', views.MoodView.as_view(), name='mood'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('dates/<int:year>/<int:month>', views.DatesDetailView.as_view(), name='dates_detail'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('admin_test/', views.admin_test_page, name='admin_test'),
]