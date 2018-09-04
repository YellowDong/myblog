from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [path(r'', views.index, name='index'),
               path(r'post/<int:pk>/', views.detail, name='detail'),
               path(r'post/<year>[0-9]{4}/<month>[0-9]{1,2}', views.archives,
                    name='archives'),
               path(r'category/<category>.*?', views.categories,
                    name='categories'), ]
