from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Post
        fields = (
            "author",
            "title",
            "slug",
            "category",
            "post_image",
            "featured",
            "ringkasan",
            "body",
            "post_status",
            "post_views",
            "created_at",
            "updated_at",
        )
