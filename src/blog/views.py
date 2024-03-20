from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from config.models import SideBar
from comment.forms import CommentForm
from comment.models import Comment
from .models import Post, Tag, Category


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"sidebars": SideBar.get_all()})
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 10
    context_object_name = "post_list"
    template_name = "blog/list.html"


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        context.update({"category": category})
        return context

    def get_queryset(self):
        """重写 queryset 根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({"tag": tag})
        return context

    def get_queryset(self):
        """重写 queryset 根据标签过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return queryset.filter(tag__id=tag_id)


class PostListView(ListView):
    queryset = Post.latest_posts()
    context_object_name = "post_list"
    template_name = "blog/list.html"


class PostDetailView(CommonViewMixin, DetailView):
    model = Post
    queryset = Post.latest_posts()
    context_object_name = "post"
    pk_url_kwarg = "post_id"
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "comment_form": CommentForm,
                "comment_list": Comment.get_by_target(self.request.path),
            }
        )
        return context


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({"keyword": self.request.GET.get("keyward", "")})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword")
        if not keyword:
            return queryset
        return queryset.filter(
            Q(title__icontains=keyword) | Q(desc__contains=keyword)
        )


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get("owner_id")
        return queryset.filter(owner_id=author_id)
