from users.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """UserCreationForm这个内置的表单是关联类django内置的User模型，我们要继承它，并重写Meta类来指定我们自己定义的User模型"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')  # django默认指定username 和password,确认密码这三个，通过这个指定自己想添加的表单控件
