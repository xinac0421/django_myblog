from django.urls import path, re_path

from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('change_email/', views.change_email, name='change_email'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),

]