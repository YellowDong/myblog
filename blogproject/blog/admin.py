from django.contrib import admin
from .models import Category, Post, Tag


# 让字段更好的展示给管理员看
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time',
                    'category', 'author']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
