from rest_framework import serializers

from .models import Post, Gallery


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category', read_only=True)

    class Meta:
        model = Post
        fields = (
            "author_name",
            "title",
            "slug",
            "category_name",
            "post_image",
            "featured",
            "ringkasan",
            "body",
            "post_status",
            "post_views",
            "created_at",
            "updated_at",
        )


class GallerySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category', read_only=True)

    class Meta:
        model = Gallery
        fields = (
            "author_name",
            "category_name",
            "caption",
            "slug",
            "gallery_image",
            "post_views",
            "created_at",
        )
