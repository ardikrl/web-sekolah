from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import TagihanSiswa, Siswa, Guru, Staff, Prestasi, MataPelajaran, NilaiMapel, Kelas


class SiswaForm(forms.ModelForm):
    tanggal_lahir = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    bio = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    nis_siswa = forms.IntegerField(label='NIS', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nomor Induk Siswa'}))
    nisn_siswa = forms.IntegerField(label='NISN', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nomor Induk Siswa Nasional'}))
    class Meta:
        model = Siswa
        fields = ('nis_siswa', 'nisn_siswa', 'pas_photo', 'nama_orang_tua', 'pekerjaan_orang_tua', 'alamat', 'tanggal_lahir', 'asal_sekolah', 'status_siswa', 'bio')


class TagihanSiswaForm(forms.ModelForm):
    tagihan = forms.IntegerField(label='NIK', required=True, widget=forms.TextInput(attrs={'placeholder': 'Total Tagihan (Rp.)'}))
    tanggal_bayar = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    class Meta:
        model = TagihanSiswa
        fields = ('siswa', 'penerima', 'keterangan', 'tanggal_bayar', 'kategori_pembayaran', 'tagihan', 'status_pembayaran')


class GuruForm(forms.ModelForm):
    tanggal_lahir = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    bio = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    nik = forms.IntegerField(label='NIK', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nomor Induk Pegawai'}))
    class Meta:
        model = Guru
        fields = ('gelar', 'pas_photo', 'nik', 'alamat', 'tanggal_lahir', 'status_guru', 'bio')


class StaffForm(forms.ModelForm):
    tanggal_lahir = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    bio = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    nip = forms.IntegerField(label='NIP', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nomor Induk Pegawai'}))
    class Meta:
        model = Staff
        fields = ('gelar', 'pas_photo', 'nip', 'alamat', 'tanggal_lahir', 'status_staff', 'bio')


class PrestasiForm(forms.ModelForm):
    tanggal_kegiatan = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    deskripsi = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    class Meta:
        model = Prestasi
        fields = ('nama_kegiatan', 'tahun_ajaran', 'tanggal_kegiatan', 'photo_cover', 'ranking_prestasi', 'tingkat_prestasi', 'deskripsi', 'pemegang_prestasi_siswa', 'pemegang_prestasi_guru')


class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ('nama', 'tahun_ajaran')


class MapelForm(forms.ModelForm):
    class Meta:
        model = MataPelajaran
        fields = ('nama', 'kelas', 'guru_pengampu', 'semester')


class NilaiMapelForm(forms.ModelForm):
    class Meta:
        model = NilaiMapel
        fields = ('mata_pelajaran', 'siswa', 'nilai_angka_1', 'nilai_huruf_1', 'deskripsi_1', 'nilai_angka_2', 'nilai_huruf_2', 'deskripsi_2')

    def __init__(self, user=None, *args, **kwargs):
        super(NilaiMapelForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['mata_pelajaran'].queryset = MataPelajaran.objects.filter(guru_pengampu__user=user)
