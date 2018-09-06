from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [path(r'', views.index, name='index'),
               path(r'post/<int:pk>/', views.detail, name='detail'),
               path(r'post/<year>/<month>', views.archives,
                    name='archives'),
               path(r'category/<int:pk>', views.categories,
                    name='categories'),
               path(r'tag/<int:pk>', views.tags, name='tags'),
               # path(r'search/', views.search, name='search'),  #这个是简单的搜索功能，搜索结果只是文章的列表，并不知道具体位置
                ]