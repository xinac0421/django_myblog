from django.urls import path, re_path

from . import views

app_name = 'tools_plugin'
urlpatterns = [
    path('', views.tools_index, name='index'),
    path('arithmetic/', views.tools_math_plugin, name='arithmetic'),
    path('arithmetic/detail', views.tools_math_plugin, name='arithmetic_detail'),
]