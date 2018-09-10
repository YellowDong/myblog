from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown
from markdown.extensions.toc import TocExtension

from django.utils.text import slugify
from django.db.models import Q
from comments.forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)  # .order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def categories(request, pk):
    # category = Category.objects.get(name=category)  # 这里用get_object_or_404更好, 参数传pk更好

    post_list = Post.objects.filter(category=pk)  # .order_by('-created_time') 这里因为在model.py的Meta类中定义了排列顺序 不需要再排列
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tags(request, pk):
    # tag = Tag.objects.get(pk=pk)
    post_list = Post.objects.filter(tags=pk)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                       'markdown.extensions.codehilite',
                                       TocExtension(slugify=slugify), ])
    post.dody = md.convert(post.body)
    post.toc = md.toc
    post.increase_views()  # 统计浏览量，即详情页每被调用一次就自动加一
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post, 'form': form, 'comment_list': comment_list}
    return render(request, 'blog/detail.html', context=context)


def search(request):
    """简单的搜索，标题或者正文中包含搜索的关键字时，
    返回文章的列表并展示在列表页,现已不用这个方法"""
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', context={'post_list': post_list, 'error_msg': error_msg})

##################################################################
##################################################################


"""以下用的是类视图，推荐使用"""

from django.views.generic import ListView, DetailView
from blog.models import Post, Category, Tag
from comments.forms import CommentForm


# 使用视图类
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """在视图函数中将模板变量传递给模板是通过render函数的context参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list}),
        这里传递一个{'post_list': post_list}字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过get_context_data获得的，
        所以我们要复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去
        """
        # 首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        curren_page = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        left_range = []
        right_range = []

        first = False
        last = False

        left_has_more = False
        right_has_more = False

        if curren_page == 1:
            right_range = page_range[curren_page:curren_page + 2]
            if right_range[-1] < total_pages:
                last = True
            if right_range[-1] + 1 < total_pages:
                right_has_more = True

        elif curren_page == total_pages:
            left_range = page_range[(curren_page-3) if (curren_page - 3) > 0 else 0:total_pages-1]
            if left_range[0] - 1 > 1:
                left_has_more = True
            if left_range[0] > 1:
                first = True

        else:
            left_range = page_range[(curren_page - 3) if (curren_page - 3) > 0 else 0:curren_page - 1]
            right_range = page_range[curren_page:curren_page+2]
            if right_range[-1] < total_pages - 1:
                right_has_more = True
            if right_range[-1] < total_pages:
                last = True
            if left_range[0] - 1 > 1:
                left_has_more = True
            if left_range[0] > 1:
                first = True
        data = {
           'left_range': left_range,
           'right_range': right_range,
           'left_has_more': left_has_more,
           'right_has_more': right_has_more,
           'last': last,
           'first': first,
        }
        return data


class CategoriesView(IndexView):
    def get_queryset(self):
        cat = get_object_or_404(Category, pk=self.kwargs.get('pk'))  # 获取分类名
        return super().get_queryset().filter(category=cat)


class TagsView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))  # 获取标签名
        return super().get_queryset().filter(tags=tag)


class ArchivesView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month'))


class DetailViews(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    # def get_object(self, queryset=None):
    #     post = super().get_object(queryset=queryset)
    #     post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all
        context.update({'form': form, 'comment_list': comment_list})
        return context






