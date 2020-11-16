import time

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sekolah.models import Prestasi, Siswa

from .forms import (CategoriForm, GalleryForm, HalamanStatisForm, PostForm,
                    PPDBForm)
from .models import Category, Gallery, HalamanStatis, Post


def home_page(request):
    data = {}
    post_list = Post.objects.filter(post_status='published').order_by('-created_at')
    paginator = Paginator(post_list, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    data["posts"] = paginator.get_page(page_number)
    data["featured_posts"] = Post.objects.filter(post_status='published', featured=True).order_by('-created_at')[:5]
    data["popular_posts"] = Post.objects.filter(post_status='published').order_by('-post_views')[:5]
    return render(request, "base.html", data)


def post_list(request):
    data = {}
    post_list = Post.objects.filter(post_status='published').order_by('-created_at')
    paginator = Paginator(post_list, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    data["posts"] = paginator.get_page(page_number)
    data["popular_posts"] = Post.objects.filter(post_status='published').order_by('-post_views')[:5]
    return render(request, "blog/public-view/list.html", data)


def post_detail(request, slug):
    data = {}
    post = Post.objects.get(slug=slug)
    data["post"] = post
    data["popular_posts"] = Post.objects.filter(post_status='published').exclude(slug=slug).order_by('-post_views')[:5]
    post.post_views = post.post_views + 1
    post.save()
    return render(request, "blog/public-view/post-detail.html", data)


def page_detail(request, slug):
    data = {}
    page = HalamanStatis.objects.get(slug=slug)
    data["page"] = page
    page.post_views = page.post_views + 1
    page.save()
    return render(request, "blog/public-view/page-detail.html", data)


def page_kontak(request):
    data = {}
    return render(request, "blog/public-view/page-kontak.html", data)


def page_ppdb(request):
    data = {}
    if request.method == "POST":
        form = PPDBForm(request.POST, request.FILES)
        if form.is_valid():
            UserModel = get_user_model()
            siswa_username = int(time.time())
            siswa_f_name = request.POST["nama_depan"]
            siswa_l_name = request.POST["nama_belakang"]
            siswa_email = "siswa@students.bunayya-school.sch.id"
            user = UserModel.objects.create_user(
                username=siswa_username,
                email=siswa_email,
                password="p455w0rd",
                first_name=siswa_f_name,
                last_name=siswa_l_name,
            )
            siswa = Siswa.objects.create(
                user=user,
                nis_siswa='',
                nisn_siswa=form.cleaned_data["nisn_siswa"],
                pas_photo=form.cleaned_data["pas_photo"],
                bio=form.cleaned_data["bio"],
                nama_orang_tua=form.cleaned_data["nama_orang_tua"],
                pekerjaan_orang_tua=form.cleaned_data["pekerjaan_orang_tua"],
                alamat=form.cleaned_data["alamat"],
                tanggal_lahir=form.cleaned_data["tanggal_lahir"],
                asal_sekolah=form.cleaned_data["asal_sekolah"],
                status_siswa='calon',
            )

        data['terkirim'] = True
    data["form"] = PPDBForm()
    return render(request, "blog/public-view/page-ppdb.html", data)


def page_prestasi(request):
    data = {}
    data["list_prestasi"] = Prestasi.objects.all().order_by(
        "-tahun_ajaran", "-tingkat_prestasi", "ranking_prestasi"
    )
    return render(request, "blog/public-view/page-prestasi.html", data)


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/web-admin')
    else:
        if not request.user.is_authenticated:
            return render(request, "blog/web-admin/admin-login.html", {})
        else:
            return HttpResponseRedirect('/web-admin')


@login_required
def admin_logout(request):
    logout(request)
    return redirect("/web-admin/login")


@login_required
def admin_dashboard(request):
    data = {}
    return render(request, "blog/web-admin/admin-base.html", data)


@login_required
def admin_berita(request):
    data = {}
    if request.user.is_staff:
        data["posts"] = Post.objects.all().order_by('-created_at')
    else:
        data["posts"] = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, "blog/web-admin/admin-berita.html", data)


@login_required
def admin_berita_add(request):
    data = {}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            berita_title = form.cleaned_data['title']
            berita_kategori = form.cleaned_data['category']
            berita_cover = form.cleaned_data['post_image']
            berita_ringkasan = form.cleaned_data['ringkasan']
            berita_isi = form.cleaned_data['body']
            berita_featured = form.cleaned_data['featured']
            berita = Post.objects.create(
                author=request.user,
                title=berita_title,
                category=berita_kategori,
                post_image=berita_cover,
                ringkasan=berita_ringkasan,
                body=berita_isi,
                featured=berita_featured,
            )

            return HttpResponseRedirect(reverse('admin_berita'))

    data["form"] = PostForm()
    return render(request, "blog/web-admin/admin-berita-add.html", data)


@login_required
def admin_berita_update(request, post_id):
    data = {}
    berita = Post.objects.get(pk=post_id)
    data["post"] = berita
    data["form"] = PostForm(instance=berita)
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None, instance=berita)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_berita'))
    return render(request, "blog/web-admin/admin-berita-update.html", data)


@login_required
def admin_berita_publish(request, post_id):
    data = {}
    post = Post.objects.get(pk=post_id)
    post.post_status = 'published'
    post.save()
    return redirect("admin_berita")


@login_required
def admin_berita_hapus(request, post_id):
    data = {}
    post = Post.objects.get(pk=post_id)
    if request.POST.get("confirm-delete"):
        post.delete()
    return redirect("admin_berita")


@login_required
def admin_kategori(request):
    data = {}
    data["kategori"] = Category.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = CategoriForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            kategori = Category.objects.create(
                name=category_name,
            )
            return HttpResponseRedirect(reverse('admin_kategori'))

    data["form"] = CategoriForm()
    return render(request, "blog/web-admin/admin-kategori.html", data)


@login_required
def admin_kategori_hapus(request, kategori_id):
    data = {}
    kategori = Category.objects.get(pk=kategori_id)
    if request.POST.get("confirm-delete"):
        kategori.delete()
    return redirect("admin_kategori")


@login_required
def admin_kategori_rename(request, kategori_id):
    data = {}
    kategori = Category.objects.get(pk=kategori_id)
    if request.method == 'POST':
        form = CategoriForm(request.POST)
        if form.is_valid():
            kategori.name = form.cleaned_data['name']
            kategori.save()
    return HttpResponseRedirect(reverse('admin_kategori'))


@login_required
def admin_halaman(request):
    data = {}
    data["halaman_statis"] = HalamanStatis.objects.all().order_by('-created_at')
    return render(request, "blog/web-admin/admin-halaman.html", data)


@login_required
def admin_halaman_add(request):
    data = {}
    if request.method == 'POST':
        form = HalamanStatisForm(request.POST, request.FILES)
        if form.is_valid():
            halaman_title = form.cleaned_data['title']
            halaman_cover = form.cleaned_data['post_image']
            halaman_isi = form.cleaned_data['body']
            halaman = HalamanStatis.objects.create(
                author=request.user,
                title=halaman_title,
                post_image=halaman_cover,
                body=halaman_isi,
            )
            return HttpResponseRedirect(reverse('admin_halaman') )
    data["form"] = HalamanStatisForm()
    return render(request, "blog/web-admin/admin-halaman-add.html", data)


@login_required
def admin_halaman_update(request, page_id):
    data = {}
    halaman = HalamanStatis.objects.get(pk=page_id)
    data["halaman"] = halaman
    data["form"] = HalamanStatisForm(instance=halaman)
    if request.method == 'POST':
        form = HalamanStatisForm(request.POST or None, request.FILES or None, instance=halaman)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_halaman'))
    return render(request, "blog/web-admin/admin-halaman-update.html", data)


@login_required
def admin_halaman_hapus(request, page_id):
    data = {}
    halaman = HalamanStatis.objects.get(pk=page_id)
    if request.POST.get("confirm-delete"):
        halaman.delete()
    return redirect("admin_halaman")


@login_required
def admin_gallery(request):
    data = {}
    data["categories"] = Category.objects.all()
    if request.user.is_staff:
        data["gallery"] = Gallery.objects.all().order_by('-created_at')
    else:
        data["gallery"] = Gallery.objects.filter(author=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get("upload-gallery"):
                gallery_caption = form.cleaned_data['caption']
                gallery_image = form.cleaned_data['gallery_image']
                gallery_category = form.cleaned_data['category']
                gallery_status = form.cleaned_data['gallery_status']
                kategori = Gallery.objects.create(
                    author=request.user,
                    caption=gallery_caption,
                    gallery_image=gallery_image,
                    category=gallery_category,
                    gallery_status=gallery_status,
                )
            return HttpResponseRedirect(reverse('admin_gallery') )
    data["form"] = GalleryForm()
    return render(request, "blog/web-admin/admin-gallery.html", data)


@login_required
def admin_gallery_update(request, gallery_id):
    data = {}
    gallery = Gallery.objects.get(pk=gallery_id)
    if request.POST.get("update-gallery"):
        gallery.caption = request.POST["caption"]
        if request.POST["category"]:
            category = Category.objects.get(pk=request.POST["category"])
            gallery.category = category
        gallery.gallery_status = request.POST['gallery_status']
        gallery.save()
    return HttpResponseRedirect(reverse('admin_gallery'))


@login_required
def admin_gallery_hapus(request, gallery_id):
    data = {}
    gallery = Gallery.objects.get(pk=gallery_id)
    if request.POST.get("confirm-delete"):
        gallery.delete()
    return redirect("admin_gallery")


@login_required
def admin_pengurus(request):
    data = {}
    UserModel = get_user_model()
    data["list_pengurus"] = UserModel.objects.all()
    if request.method == "POST":
        nama_depan = request.POST.get("nama_depan")
        nama_belakang = request.POST.get("nama_belakang")
        username = request.POST.get("username")
        password = request.POST.get("password")
        status_pengurus = request.POST.get("status_pengurus")
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            user = UserModel.objects.create_user(
                first_name=nama_depan,
                last_name=nama_belakang,
                username=username,
                password=password
            )
            if status_pengurus == 'petugas':
                user.is_staff = True
                user.save()
        return redirect("admin_pengurus")

    return render(request, "blog/web-admin/admin-pengurus.html", data)


@login_required
def admin_pengurus_update(request, pengurus_id):
    data = {}
    UserModel = get_user_model()
    pengurus = UserModel.objects.get(pk=pengurus_id)
    if request.POST.get("confirm-update"):
        pengurus.first_name = request.POST.get("nama_depan")
        pengurus.last_name = request.POST.get("nama_belakang")
        pengurus.username = request.POST.get("username")
        if request.POST.get("password"):
            pengurus.set_password(request.POST.get("password"))
        pengurus.save()
        return HttpResponseRedirect(reverse('admin_pengurus'))
    return render(request, "blog/web-admin/admin-pengurus.html")


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
