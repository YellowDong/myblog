from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """拓展用户模型有两种方式， 一种是通过继承抽象类AbstractUser然后增加一些自定义的字段（因为django内置的User模型只提供类基本的
    字段，如username, password, email有时候并没有达到我们自己的需求）
    另一种方式是通过Profile 模式拓展用户模型，这种情况是一开始没有用自定义模型，而用类内置User模型，现在在内置模型的基础上进行扩展
    (其实就是一种关联数据表的方式，通过另外建一张表来记录用户自定义的字段，然后通过外键关联)"""
    nickname = models.CharField(max_length=20, blank=True)

    class Meta(AbstractUser.Meta):
        pass

# 方法二
# from django.contrib.auth.models import User
#
#
# class Profile(models.Model):
#     nickname = models.CharField(max_length=50, blank=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

