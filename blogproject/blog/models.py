from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 分类名已经存在的情况下不能创建相同的分类名所以增加unique=True

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now_add=True)
    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)# 这里有一个坑，在定义自己的User模型时，必须也把这个author字段关联的User模型更换
    # 新增一个字段用来记录文章的浏览量(新增字段记得重新迁移数据库)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 根据pk值获取具体谋篇文章的url
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time', 'title']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])  # 部分更新通过update_fields添加需要更新的字段

    def save(self, *args, **kwargs):
        # 如果没有填写摘要，则截取内容的前54个字符作为摘要
        if not self.excerpt:
            # 实例化一个Markdown类,用于渲染body文本
            md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
            # strip_tag方法是将HTML文本中的HTML标签去掉
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)


