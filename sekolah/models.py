from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField

SEMESTER_CHOICES = (
    ("semester 1", "Semester 1"),
    ("semester 2", "Semester 2"),
)


class TahunPelajaran(models.Model):
    tahun = models.CharField(max_length=4, default='2020')
    def __str__(self):
        try:
            return f"{self.tahun}/{int(self.tahun)+1}"
        except ValueError:
            return ''


class Sekolah(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    visi = models.TextField()
    misi = models.TextField()
    sejarah = models.TextField()

    slug = AutoSlugField(populate_from="id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "sekolah"


class KepalaSekolah(models.Model):
    sekolah = models.ForeignKey(Sekolah, on_delete=models.CASCADE)
    guru = models.ForeignKey("Guru", on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey(TahunPelajaran, default='2020', on_delete=models.CASCADE)

    def __str__(self):
        return self.guru.user.get_full_name()
    
    class Meta:
        verbose_name_plural = "Kepala Sekolah"


class Kelas(models.Model):
    nama = models.CharField(max_length=50)
    tahun_ajaran = models.ForeignKey(TahunPelajaran, default='2020', on_delete=models.CASCADE)
    siswa = models.ManyToManyField("Siswa", related_name="daftar_siswa", blank=True)
    slug = AutoSlugField(populate_from="id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} - {self.tahun_ajaran}"

    class Meta:
        verbose_name_plural = "kelas"


class WaliKelas(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    guru = models.ForeignKey("Guru", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.guru.user.get_full_name()}, {self.guru.gelar}"
    
    class Meta:
        verbose_name_plural = "Wali Kelas"


class Guru(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gelar = models.CharField(max_length=7, blank=True, null=True, default='S.Pd.')
    pas_photo = models.ImageField(upload_to="photo-guru", blank=True, null=True)
    nik = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    alamat = models.CharField(max_length=30, blank=True, null=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    STATUS_CHOICES = (
        ("lepas", "Lepas"),
        ("tetap", "Tetap"),
        ("keluar", "Keluar"),
    )
    status_guru = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="tetap",
        blank=True,
        null=True,
    )
    slug = AutoSlugField(populate_from="id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.gelar:
            return f"{self.user.get_full_name()}, {self.gelar}"
        else:
            return self.user.get_full_name()

    class Meta:
        verbose_name_plural = "guru"


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gelar = models.CharField(max_length=7, blank=True, null=True, default='S.Pd.')
    pas_photo = models.ImageField(upload_to="photo-guru", blank=True, null=True)
    nip = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    alamat = models.CharField(max_length=30, blank=True, null=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    STATUS_CHOICES = (
        ("lepas", "Lepas"),
        ("tetap", "Tetap"),
        ("keluar", "Keluar"),
    )
    status_staff = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="tetap",
        blank=True,
        null=True,
    )
    slug = AutoSlugField(populate_from="id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.gelar:
            return f"{self.user.get_full_name()}, {self.gelar}"
        else:
            return self.user.get_full_name()

    class Meta:
        verbose_name_plural = "staff"


class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nis_siswa = models.CharField(max_length=15, unique=True, default='')
    nisn_siswa = models.CharField(max_length=15, unique=True, default='')
    pas_photo = models.ImageField(upload_to="photo-siswa", blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    nama_orang_tua = models.CharField(max_length=50, blank=True, null=True)
    no_hp = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pekerjaan_orang_tua = models.CharField(max_length=50, blank=True, null=True)
    alamat = models.CharField(max_length=30, blank=True, null=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    asal_sekolah = models.CharField(max_length=100, blank=True, null=True)
    STATUS_CHOICES = (
        ("calon", "Calon"),
        ("tetap", "Tetap"),
        ("pindah", "Pindah"),
        ("alumni", "Alumni"),
    )
    status_siswa = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="tetap",
        null=True,
        blank=True,
    )

    slug = AutoSlugField(populate_from="id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name_plural = "siswa"


class TagihanSiswa(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    penerima = models.ForeignKey(Staff, on_delete=models.RESTRICT)
    keterangan = models.CharField(max_length=255)
    KATEGORI_CHOICES = (
        ("spp", "SPP Bulanan"),
        ("tahunan", "Biaya Tahunan"),
        ("kegiatan", "Biaya Kegiatan Siswa"),
        ("buku", "Biaya Buku Siswa"),
        ("lainnya", "Biaya Lainnya"),
    )
    kategori_pembayaran = models.CharField(
        max_length=25,
        choices=KATEGORI_CHOICES,
        default="spp",
    )
    STATUS_CHOICES = (
        ("lunas", "Lunas"),
        ("belum-lunas", "Belum Lunas"),
        ("belum-dibayar", "Belum Dibayar"),
    )
    status_pembayaran = models.CharField(
        max_length=25,
        choices=KATEGORI_CHOICES,
        default="lunas",
    )
    tanggal_bayar = models.DateTimeField(auto_now_add=True)
    tanggal_diubah = models.DateTimeField(auto_now=True)
    tagihan = models.IntegerField(max_digits=10)


class Prestasi(models.Model):
    nama_kegiatan = models.CharField(max_length=30, blank=True, null=True)
    photo_cover = models.ImageField(upload_to="photo-prestasi", blank=True, null=True)
    deskripsi = models.TextField(max_length=500, blank=True, null=True)
    tanggal_kegiatan = models.DateField(null=True, blank=True)
    RANKING_CHOICES = (
        ("a", "Juara Umum"),
        ("b", "Juara I"),
        ("c", "Juara II"),
        ("d", "Juara III"),
        ("e", "Juara Harapan"),
        ("f", "Juara Harapan I"),
        ("g", "Juara Harapan II"),
        ("h", "Juara Harapan III"),
    )
    ranking_prestasi = models.CharField(
        max_length=20,
        choices=RANKING_CHOICES,
        default="juara-umum",
        blank=True,
        null=True,
    )
    TINGKAT_CHOICES = (
        ("a", "Sekolah"),
        ("b", "Desa"),
        ("c", "Kecamatan"),
        ("d", "Kabupaten"),
        ("e", "Provinsi"),
        ("f", "Nasional"),
        ("g", "Internasional"),
    )
    tingkat_prestasi = models.CharField(
        max_length=15,
        choices=TINGKAT_CHOICES,
        default="sekolah",
        blank=True,
        null=True,
    )
    tahun_ajaran = models.ForeignKey(TahunPelajaran, default='2020', on_delete=models.CASCADE)
    pemegang_prestasi_siswa = models.ManyToManyField(Siswa, blank=True)
    pemegang_prestasi_guru = models.ManyToManyField(Guru, blank=True)

    slug = AutoSlugField(populate_from="id")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_kegiatan
    
    def tingkat_verbose(self):
        return dict(Prestasi.TINGKAT_CHOICES)[self.tingkat_prestasi]
    
    def ranking_verbose(self):
        return dict(Prestasi.RANKING_CHOICES)[self.ranking_prestasi]

    class Meta:
        verbose_name_plural = "Prestasi Sekolah"


class MataPelajaran(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)
    kelas = models.ForeignKey(Kelas, null=True, blank=True, on_delete=models.SET_NULL)
    guru_pengampu = models.ForeignKey(Guru, null=True, blank=True, on_delete=models.SET_NULL)
    semester = models.CharField(
        max_length=10,
        default='semester 1',
        choices=SEMESTER_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nama

    def get_guru(self):
        if self.guru_pengampu:
            return f"{self.guru_pengampu.user.get_full_name()} {self.guru_pengampu.gelar}"
        else:
            return ''

    class Meta:
        verbose_name_plural = "Mata Pelajaran"


class NilaiMapel(models.Model):
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    nilai_angka_1 = models.IntegerField(blank=True, null=True, default=0)
    nilai_angka_2 = models.IntegerField(blank=True, null=True, default=0)
    NILAI_CHOICES = (
        ("a", "Sangat Baik"),
        ("b", "Baik"),
        ("c", "Cukup"),
        ("d", "Kurang"),
    )
    nilai_huruf_1 = models.CharField(
        max_length=15,
        default='d',
        choices=NILAI_CHOICES,
        blank=True,
        null=True,
    )
    nilai_huruf_2 = models.CharField(
        max_length=15,
        default='d',
        choices=NILAI_CHOICES,
        blank=True,
        null=True,
    )
    deskripsi_1 = models.CharField(max_length=150, blank=True, null=True)
    deskripsi_2 = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.mata_pelajaran.nama
    
    class Meta:
        verbose_name_plural = "Nilai Mata Pelajaran"
