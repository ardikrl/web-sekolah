from django.contrib import admin
from django.db.models import Max

from .models import (
    Sekolah,
    KepalaSekolah,
    Kelas,
    WaliKelas,
    Staff,
    Guru,
    Siswa,
    TagihanSiswa,
    Prestasi,
    MataPelajaran,
    NilaiMapel
)


class SekolahAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "kepala_sekolah",
        "visi",
        "misi",
        "sejarah",
    )
    def kepala_sekolah(self, obj):
        return obj.kepalasekolah_set.filter(sekolah=obj).order_by('-tahun_ajaran').first()
admin.site.register(Sekolah, SekolahAdmin)


class KepalaSekolahAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "nama_sekolah",
        "tahun_ajaran",
    )
    def nama_sekolah(self, obj):
        return obj.sekolah.nama
    def nama(self, obj):
        return obj.guru.user.get_full_name()
admin.site.register(KepalaSekolah, KepalaSekolahAdmin)


class KelasAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "tahun_ajaran",
        "wali_kelas"
    )
    def wali_kelas(self, obj):
        return obj.walikelas_set.get(tahun_ajaran=obj.tahun_ajaran)
admin.site.register(Kelas, KelasAdmin)


class WaliKelasAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "nama_kelas",
    )
    def nama(self, obj):
        return obj.guru.user.get_full_name()
    def nama_kelas(self, obj):
        return obj.kelas.nama
    def tahun_ajaran(self, obj):
        return obj.kelas.tahun_ajaran
admin.site.register(WaliKelas, WaliKelasAdmin)


class GuruAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "nik",
        "status_guru",
    )
    def nama(self, obj):
        return obj.user.get_full_name()
admin.site.register(Guru, GuruAdmin)


class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "nip",
        "status_staff",
    )
    def nama(self, obj):
        return obj.user.get_full_name()
admin.site.register(Staff, StaffAdmin)


class SiswaAdmin(admin.ModelAdmin):
    list_display = (
        "nis_siswa",
        "nisn_siswa",
        "nama",
    )
    def nama(self, obj):
        return obj.user.get_full_name()
admin.site.register(Siswa, SiswaAdmin)


class TagihanSiswaAdmin(admin.ModelAdmin):
    list_display = (
        "tanggal_bayar",
        "nama_siswa",
        "nama_penerima",
        "kategori_pembayaran",
        "status_pembayaran",
        "tagihan",
    )
    def nama_siswa(self, obj):
        return obj.siswa.user.get_full_name()
    def nama_penerima(self, obj):
        return obj.penerima.user.get_full_name()
admin.site.register(TagihanSiswa, TagihanSiswaAdmin)


class PrestasiAdmin(admin.ModelAdmin):
    list_display = (
        "nama_kegiatan",
        "tahun_ajaran",
        "tingkat_prestasi",
        "ranking_prestasi",
    )
admin.site.register(Prestasi, PrestasiAdmin)


class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "tahun_pelajaran",
        "kelas",
        "guru_pengampu",
    )
    def tahun_pelajaran(self, obj):
        return obj.get_tahun()
    def guru_pengampu(self, obj):
        return obj.get_guru()
admin.site.register(MataPelajaran, MataPelajaranAdmin)


class NilaiMapelAdmin(admin.ModelAdmin):
    list_display = (
        "tahun_pelajaran",
        "mata_pelajaran",
        "siswa",
        "nilai_angka_1",
        "nilai_angka_2",
        "nilai_huruf_1",
        "nilai_huruf_2",
        "deskripsi_1",
        "deskripsi_2",
    )
    def tahun_pelajaran(self, obj):
        return obj.mata_pelajaran.get_tahun()
admin.site.register(NilaiMapel, NilaiMapelAdmin)
