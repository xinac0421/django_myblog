from django.contrib import admin
from .models import Article, Tag, Category
from django.db.models import F


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'create_time', 'is_publish']

    """
    def save_model(self, request, obj, form, change):
        obj.save()
        if change:
            obj_tag_list = obj.tags.all()
            for obj_tag in obj_tag_list:
                tag_number = obj_tag.article_set.count()
                obj_tag.count = tag_number
                obj_tag.save()
        else:
            if request.method == 'POST':
                article_tag_list = request.POST.getlist('tags')
                for tid in article_tag_list:
                    obj_tag = Tag.objects.get(pk=int(tid))
                    obj_tag.count = F('count') + 1
                    obj_tag.save()
    """


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
