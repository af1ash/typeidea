from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
from .adminforms import PostAdminForm
from .models import Post, Category, Tag

# Register your models here.
class PostInline(admin.TabularInline):  # StackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1       # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器只展示当前用户的分类
    """
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'owner', 'status', 'created_time', 'operator')

    list_display_links = []

    list_filter = [
        CategoryOwnerFilter
    ]
    search_fields = ['title', 'category__name']
    exclude = ('owner', )

    actions_on_top = True
    actions_on_bottom = True


    # 编辑界面
    save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content'
            ),
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', )
        })
    )

    filter_horizontal = ('tag', )

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))
    
    operator.short_description = '操作'

    # def post_count(self, obj):
    #     return obj.post_set.count()
    
    # post_count.short_description = '文章数量'

    # class Media:
    #     css = {
    #         'all': (
    #             "https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", 
    #         ),
    #     }
    #     js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js", )