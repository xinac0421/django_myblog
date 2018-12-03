from django.urls import path, re_path

from . import views

app_name = 'comment'
urlpatterns = [
    path('', views.comment_update, name='comment'),
]