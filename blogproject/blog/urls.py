from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [path(r'', views.index, name='index'),
               path(r'post/<int:pk>/', views.detail, name='detail'),
               path(r'post/<year>/<month>', views.archives,
                    name='archives'),
               path(r'category/<category>', views.categories,
                    name='categories'),
               path(r'tag/<int:pk>', views.tags, name='tags'), ]
