"""
Django settings for mysite1810 project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',  # 富文本编辑器
    'ckeditor_uploader',  # 文件上传
    'gregblog.apps.GregblogConfig',  # 博客app
    'count_statistics',     # 统计计数app
    'tools_plugin.apps.ToolsPluginConfig',  # 其他小工具类的app
    'comment.apps.CommentConfig',  # 评论app
    'user.apps.UserConfig',  # 用户app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite1810.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite1810.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 设置语言

TIME_ZONE = 'Asia/Shanghai'  # 设置时区为上海，只有下面的USE_TZ设置为False时，这项才生效

USE_I18N = True

USE_L10N = True

# USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

INTERNAL_IPS = ('127.0.0.1',)

# media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 配置ckeditor
CKEDITOR_UPLOAD_PATH = 'ckeditor_upload/'  # 该编辑器的上传路径是相对于设置的的MEDIA_ROOT路径
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default': {
        'width': 'auto',
        'toolbar': (
            ['div', 'Source', '-', 'Preview'],
            ['Copy', 'Cut', 'Paste', 'PasteText', 'PasteFromWord',],
            ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About'],
            ['CodeSnippet', '-', 'Print'],
        ),

        # 插件
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils', ]),
    },

    'comment_ckeditor': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['TextColor', 'BGColor', 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Smiley', 'SpecialChar', 'Blockquote'],
        ],
        'width': 'auto',
        'height': '180',
        'tabSpaces': 4,
        'removePlugins': 'elementspath',
        'resize_enabled': False,

    }
}

# 设置自定义全局参数
EACH_PAGES_PER = 10   # 设置每页显示数量
PAGES_GAP_NUMBER = 2  # 设置分页栏的当前页前后显示间距

# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',  # 缓存表名
    }
}

