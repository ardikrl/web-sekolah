from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'galleries', views.GalleryViewSet)

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("berita/", views.post_list, name="post_list"),
    path("berita/<str:slug>", views.post_detail, name="post_detail"),
    path("page/prestasi", views.page_prestasi, name="page_prestasi"),
    path("page/kontak", views.page_kontak, name="page_kontak"),
    path("page/ppdb", views.page_ppdb, name="page_ppdb"),
    path("page/<str:slug>", views.page_detail, name="page_detail"),
    path("web-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("web-admin/login", views.admin_login, name="admin_login"),
    path("web-admin/logout", views.admin_logout, name="admin_logout"),
    path("web-admin/berita", views.admin_berita, name="admin_berita"),
    path("web-admin/berita/tambah", views.admin_berita_add, name="admin_berita_add"),
    path("web-admin/berita/<int:post_id>/update", views.admin_berita_update, name="admin_berita_update"),
    path("web-admin/berita/<int:post_id>/publish", views.admin_berita_publish, name="admin_berita_publish"),
    path("web-admin/berita/<int:post_id>/hapus", views.admin_berita_hapus, name="admin_berita_hapus"),
    path("web-admin/kategori", views.admin_kategori, name="admin_kategori"),
    path("web-admin/kategori/<int:kategori_id>/hapus", views.admin_kategori_hapus, name="admin_kategori_hapus"),
    path("web-admin/kategori/<int:kategori_id>/rename", views.admin_kategori_rename, name="admin_kategori_rename"),
    path("web-admin/halaman", views.admin_halaman, name="admin_halaman"),
    path("web-admin/halaman/tambah", views.admin_halaman_add, name="admin_halaman_add"),
    path("web-admin/halaman/<int:page_id>/update", views.admin_halaman_update, name="admin_halaman_update"),
    path("web-admin/halaman/<int:page_id>/hapus", views.admin_halaman_hapus, name="admin_halaman_hapus"),
    path("web-admin/gallery", views.admin_gallery, name="admin_gallery"),
    path("web-admin/gallery/<int:gallery_id>/hapus", views.admin_gallery_hapus, name="admin_gallery_hapus"),
    path("web-admin/gallery/<int:gallery_id>/update", views.admin_gallery_update, name="admin_gallery_update"),
    path("web-admin/bank-data/admin-pengurus", views.admin_pengurus, name="admin_pengurus"),
    path("web-admin/bank-data/admin-pengurus/<int:pengurus_id>/update", views.admin_pengurus_update, name="admin_pengurus_update"),
    path("web-admin/bank-data/admin-pengurus/<int:pengurus_id>/hapus", views.admin_pengurus_hapus, name="admin_pengurus_hapus"),
    # api urls
    path('api/', include(router.urls)),
]
