from django.contrib import admin
from .models import ReadDateDetail, ReadNum
# Register your models here.


@admin.register(ReadNum)
class AdminReadNum(admin.ModelAdmin):
    list_display = ['read_num', 'content_object']


@admin.register(ReadDateDetail)
class AdminReadDateDetail(admin.ModelAdmin):
    list_display = ['date', 'read_num', 'content_object']
