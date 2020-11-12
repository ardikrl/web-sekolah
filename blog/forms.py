from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Post, Category, HalamanStatis, Gallery
from sekolah.models import Siswa


STATUS_CHOICES = [
    ("draft", "Draft"),
    ("published", "Published"),
]
GALLERY_STATUS_CHOICES = [
    ("private", "Private"),
    ("public", "Public"),
]

class CategoriForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)


class PostForm(forms.ModelForm):
    ringkasan = forms.CharField(label="Ringkasan", max_length=150, required=True)
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = ('title', 'category', 'post_image', 'ringkasan', 'body', 'featured')


class HalamanStatisForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = HalamanStatis
        fields = ('title', 'post_image', 'body')


class GalleryForm(forms.ModelForm):
    gallery_status = forms.CharField(widget=forms.Select(choices=GALLERY_STATUS_CHOICES))
    class Meta:
        model = Gallery
        fields = ('caption', 'gallery_image', 'category', 'gallery_status')


class PPDBForm(forms.ModelForm):
    tanggal_lahir = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    nama_orang_tua = forms.CharField(label='Nama Orang Tua', required=False)
    pekerjaan_orang_tua = forms.CharField(label='Pekerjaan Orang Tua', required=False)
    no_hp = forms.CharField(label='No HP', widget=forms.TextInput(attrs={'placeholder': '081-2222-90905'}), required=False)
    email = forms.EmailField(label='Alamat E-Mail', widget=forms.EmailInput(attrs={'placeholder': 'nama@website.com'}), required=False)
    bio = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 120, 'rows': 30}), required=False)
    nisn_siswa = forms.IntegerField(label='NISN (Nomor Induk Siswa Nasional)', required=False)
    pas_photo = forms.CharField(label='PAS Photo (3x4)', required=True)
    class Meta:
        model = Siswa
        fields = ('nisn_siswa', 'pas_photo', 'nama_orang_tua', 'pekerjaan_orang_tua', 'no_hp', 'email', 'alamat', 'tanggal_lahir', 'asal_sekolah', 'bio')
