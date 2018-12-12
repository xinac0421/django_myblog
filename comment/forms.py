import bleach
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(
        max_length=200,
        widget=CKEditorWidget(config_name='comment_ckeditor'),

        label=False,
        error_messages={
            'required': '评论内容不能为空',
            'max_length': '评论内容不能超过200个字符',
        }
    )
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        # 获取views中实例化时传入的user参数，使用完需删除不影响父类
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        super(CKEditorWidget)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('您还未登录,登录后可评论')

        # 判断用户是否认证
        if not self.user.get_email_active():
            raise forms.ValidationError('您还没有认证通过，请先去个人中心认证!')

        # 判断内容是否为空
        input_text = self.cleaned_data.get('text', '')
        input_text = bleach.clean(input_text, strip=True)  # 去除html标签和特殊字符
        if input_text.strip() == '':
            raise forms.ValidationError('评论内容不能为空')

        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['model_obj'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论的文章不存在或被删除')
        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data.get('reply_comment_id', '')
        if reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复的记录不存在')
        return reply_comment_id


