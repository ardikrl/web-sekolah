from django.contrib import admin

from .models import Category, Post, HalamanStatis, Gallery


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_at",
    )
admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "post_status",
        "featured",
        "slug",
        "created_at",
        "updated_at",
    )
admin.site.register(Post, PostAdmin)


class HalamanStatisAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "slug",
        "created_at",
        "updated_at",
    )
admin.site.register(HalamanStatis, HalamanStatisAdmin)


class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        "caption",
        "category",
        "created_at",
    )
admin.site.register(Gallery, GalleryAdmin)
