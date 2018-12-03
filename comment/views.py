import bleach
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm

# Create your views here.


def comment_update(request):
    comment_form = CommentForm(request.POST, user=request.user)
    ajax_data = {}

    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['model_obj']

        # 判断是不是回复
        parent = comment_form.cleaned_data.get('parent', None)
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 返回数据给前端ajax
        ajax_data['status'] = 'SUCCESS'
        ajax_data['username'] = comment.user.get_nickname_or_username()
        ajax_data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        ajax_data['text'] = comment.text
        if parent is not None:
            ajax_data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            ajax_data['reply_to'] = ''
        ajax_data['pk'] = comment.pk
        ajax_data['root_pk'] = comment.root.pk if comment.root is not None else ''

    else:
        ajax_data['status'] = 'ERROR'
        ajax_data['error_message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(ajax_data)
