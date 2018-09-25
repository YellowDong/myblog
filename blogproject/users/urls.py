from django.urls import path
from users.views import register, index

app_name = 'users'
urlpatterns = [
    path(r'register/', register, name='register'),
    path(r'', index, name='index'),
    # path(r'', reset_password, name='reset_password')
]