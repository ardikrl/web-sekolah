from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from="name")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL
    )
    post_image = models.ImageField(upload_to="post-cover", blank=True, null=True)
    featured = models.BooleanField(default=False)
    ringkasan = models.CharField(max_length=150)
    body = RichTextUploadingField()
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    post_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )
    post_views=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def status_verbose(self):
        return dict(Post.STATUS_CHOICES)[self.post_status]


@receiver(post_delete, sender=Post)  # hapus file gambar setelah post-nya dihapus
def submission_delete(sender, instance, **kwargs):
    instance.post_image.delete(False)


class HalamanStatis(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True)
    post_image = models.ImageField(upload_to="post-cover", blank=True, null=True)
    body = RichTextUploadingField()
    post_views=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from="caption")
    gallery_image = models.ImageField(upload_to="post-gallery")
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL
    )
    STATUS_CHOICES = (
        ("private", "Private"),
        ("public", "Public"),
    )
    gallery_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="public",
    )
    post_views=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "galleries"


@receiver(post_delete, sender=Gallery)  # hapus file gambar setelah gallery-nya dihapus
def submission_delete(sender, instance, **kwargs):
    instance.gallery_image.delete(False)
