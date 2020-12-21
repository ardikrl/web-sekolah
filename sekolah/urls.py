from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'tagihan', views.TagihanViewSet)

urlpatterns = [
    # admin siswa
    path("web-admin/siswa", views.admin_siswa, name="admin_siswa"),
    path("web-admin/siswa/add", views.admin_siswa_add, name="admin_siswa_add"),
    path("web-admin/siswa/<int:siswa_id>/detail", views.admin_siswa_detail, name="admin_siswa_detail"),
    path("web-admin/siswa/<int:siswa_id>/update", views.admin_siswa_update, name="admin_siswa_update"),
    path("web-admin/siswa/<int:siswa_id>/hapus", views.admin_siswa_hapus, name="admin_siswa_hapus"),
    # admin tagihan pembayaran
    path("web-admin/tagihan", views.admin_tagihan, name="admin_tagihan"),
    path("web-admin/tagihan/add", views.admin_tagihan_add, name="admin_tagihan_add"),
    path("web-admin/tagihan/<int:tagihan_id>/detail", views.admin_tagihan_detail, name="admin_tagihan_detail"),
    path("web-admin/tagihan/<int:tagihan_id>/update", views.admin_tagihan_update, name="admin_tagihan_update"),
    path("web-admin/tagihan/<int:tagihan_id>/hapus", views.admin_tagihan_hapus, name="admin_tagihan_hapus"),
    # admin guru
    path("web-admin/guru", views.admin_guru, name="admin_guru"),
    path("web-admin/guru/add", views.admin_guru_add, name="admin_guru_add"),
    path("web-admin/guru/<int:guru_id>/detail", views.admin_guru_detail, name="admin_guru_detail"),
    path("web-admin/guru/<int:guru_id>/update", views.admin_guru_update, name="admin_guru_update"),
    path("web-admin/guru/<int:guru_id>/hapus", views.admin_guru_hapus, name="admin_guru_hapus"),
    # admin prestasi
    path("web-admin/prestasi", views.admin_prestasi, name="admin_prestasi"),
    path("web-admin/prestasi/add", views.admin_prestasi_add, name="admin_prestasi_add"),
    path("web-admin/prestasi/<int:prestasi_id>/detail", views.admin_prestasi_detail, name="admin_prestasi_detail"),
    path("web-admin/prestasi/<int:prestasi_id>/update", views.admin_prestasi_update, name="admin_prestasi_update"),
    path("web-admin/prestasi/<int:prestasi_id>/hapus", views.admin_prestasi_hapus, name="admin_prestasi_hapus"),
    # bank data
    path("web-admin/bank-data", views.admin_bank_data, name="admin_bank_data"),
    path("web-admin/tahun-ajaran", views.admin_tahun_ajaran, name="admin_tahun_ajaran"),
    path("web-admin/tahun-ajaran/<int:tahun_id>/update", views.admin_tahun_ajaran_update, name="admin_tahun_ajaran_update"),
    path("web-admin/tahun-ajaran/<int:tahun_id>/hapus", views.admin_tahun_ajaran_hapus, name="admin_tahun_ajaran_hapus"),
    # kelas
    path("web-admin/kelas", views.admin_kelas, name="admin_kelas"),
    path("web-admin/kelas/add", views.admin_kelas_add, name="admin_kelas_add"),
    path("web-admin/kelas/<int:kelas_id>/add-siswa", views.admin_kelas_siswa, name="admin_kelas_siswa"),
    path("web-admin/kelas/<int:kelas_id>/update-wali", views.admin_kelas_wali, name="admin_kelas_wali"),
    path("web-admin/kelas/<int:kelas_id>/detail", views.admin_kelas_detail, name="admin_kelas_detail"),
    path("web-admin/kelas/<int:kelas_id>/update", views.admin_kelas_update, name="admin_kelas_update"),
    path("web-admin/kelas/<int:kelas_id>/hapus", views.admin_kelas_hapus, name="admin_kelas_hapus"),
    # mapel
    path("web-admin/mapel", views.admin_mapel, name="admin_mapel"),
    path("web-admin/mapel/add", views.admin_mapel_add, name="admin_mapel_add"),
    path("web-admin/mapel/<int:mapel_id>/detail", views.admin_mapel_detail, name="admin_mapel_detail"),
    path("web-admin/mapel/<int:mapel_id>/update", views.admin_mapel_update, name="admin_mapel_update"),
    path("web-admin/mapel/<int:mapel_id>/hapus", views.admin_mapel_hapus, name="admin_mapel_hapus"),
    path("web-admin/mapel/<int:mapel_id>/template", views.admin_mapel_nilai_template, name="admin_mapel_nilai_template"),
    path("web-admin/mapel/<int:mapel_id>/import", views.admin_mapel_nilai_import, name="admin_mapel_nilai_import"),
    # api urls
    path('api/', include(router.urls)),
]
