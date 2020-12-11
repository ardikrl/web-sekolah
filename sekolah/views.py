from io import BytesIO
import time

import xlsxwriter
import xlrd
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

from .forms import (
    GuruForm,
    KelasForm,
    MapelForm,
    NilaiMapelForm,
    PrestasiForm,
    SiswaForm,
    TagihanSiswaForm,
)

from .models import (
    Guru,
    Kelas,
    WaliKelas,
    MataPelajaran,
    NilaiMapel,
    Prestasi,
    Siswa,
    TagihanSiswa,
    TahunPelajaran,
)


@login_required
def admin_tahun_ajaran(request):
    data = {}
    data["list_tahun"] = TahunPelajaran.objects.all().order_by("-tahun")
    if request.POST.get("add-tp"):
        TahunPelajaran.objects.create(tahun=request.POST["tahun"])
        return redirect("admin_tahun_ajaran")
    return render(request, "sekolah/web-admin/admin-tahun-ajaran.html", data)


@login_required
def admin_tahun_ajaran_update(request, tahun_id):
    if request.POST.get("confirm-update"):
        tahun = TahunPelajaran.objects.get(pk=tahun_id)
        tahun.tahun = request.POST["tahun"]
        tahun.save()
        return redirect("admin_tahun_ajaran")


@login_required
def admin_tahun_ajaran_hapus(request, tahun_id):
    if request.POST.get("confirm-delete"):
        tahun = TahunPelajaran.objects.get(pk=tahun_id)
        tahun.delete()
        return redirect("admin_tahun_ajaran")


@login_required
def admin_siswa(request):
    data = {}
    list_siswa = Siswa.objects.filter(status_siswa = 'aktif')
    if request.GET.get('filter'):
        if request.GET.get('filter') == 'aktif':
            list_siswa = Siswa.objects.filter(Q(status_siswa='tetap') | Q(status_siswa='pindah'))
        else:
            list_siswa = Siswa.objects.filter(status_siswa=request.GET.get('filter'))
    data["list_siswa"] = list_siswa.order_by("nis_siswa")

    return render(request, "sekolah/web-admin/admin-siswa.html", data)


# siswa
@login_required
def admin_siswa_add(request):
    data = {}
    if request.method == "POST":
        form = SiswaForm(request.POST, request.FILES)
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
                nis_siswa=form.cleaned_data["nis_siswa"],
                nisn_siswa=form.cleaned_data["nisn_siswa"],
                pas_photo=form.cleaned_data["pas_photo"],
                bio=form.cleaned_data["bio"],
                nama_orang_tua=form.cleaned_data["nama_orang_tua"],
                pekerjaan_orang_tua=form.cleaned_data["pekerjaan_orang_tua"],
                alamat=form.cleaned_data["alamat"],
                tanggal_lahir=form.cleaned_data["tanggal_lahir"],
                asal_sekolah=form.cleaned_data["asal_sekolah"],
                status_siswa=form.cleaned_data["status_siswa"],
            )

        return redirect("admin_siswa")
    data["form"] = SiswaForm()
    return render(request, "sekolah/web-admin/admin-siswa-add.html", data)


@login_required
def admin_siswa_detail(request, siswa_id):
    data = {}
    data["siswa"] = Siswa.objects.get(pk=siswa_id)
    return render(request, "sekolah/web-admin/admin-siswa-detail.html", data)


@login_required
def admin_siswa_update(request, siswa_id):
    data = {}
    siswa = Siswa.objects.get(pk=siswa_id)
    data["siswa"] = siswa
    data["form"] = SiswaForm(instance=siswa)
    if request.method == "POST":
        form = SiswaForm(request.POST or None, instance=siswa)
        if form.is_valid():
            siswa_f_name = request.POST["nama_depan"]
            siswa_l_name = request.POST["nama_belakang"]
            user = siswa.user
            user.first_name = siswa_f_name
            user.last_name = siswa_l_name
            user.save()
            form.save()
            return redirect("admin_siswa_detail", siswa_id=siswa_id)
    return render(request, "sekolah/web-admin/admin-siswa-update.html", data)


@login_required
def admin_siswa_hapus(request, siswa_id):
    data = {}
    siswa = Siswa.objects.get(pk=siswa_id)
    siswa_user = siswa.user
    if request.POST.get("confirm-delete"):
        siswa_user.delete()
        siswa.delete()
    return redirect("admin_siswa")


# tagihan siswa
@login_required
def admin_tagihan(request):
    data = {}
    list_tagihan = TagihanSiswa.objects.all()
    if request.GET.get('filter'):
        list_tagihan = TagihanSiswa.objects.filter(status_pembayaran=request.GET.get('filter'))
    data["list_tagihan"] = list_tagihan.order_by("-tanggal_bayar")

    return render(request, "sekolah/web-admin/admin-tagihan.html", data)


@login_required
def admin_tagihan_add(request):
    data = {}
    if request.method == "POST":
        form = TagihanSiswaForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("admin_tagihan")
    data["form"] = TagihanSiswaForm()
    return render(request, "sekolah/web-admin/admin-tagihan-add.html", data)


@login_required
def admin_tagihan_detail(request, tagihan_id):
    data = {}
    data["tagihan"] = TagihanSiswa.objects.get(pk=tagihan_id)
    return render(request, "sekolah/web-admin/admin-tagihan-detail.html", data)


@login_required
def admin_tagihan_update(request, tagihan_id):
    data = {}
    tagihan = TagihanSiswa.objects.get(pk=tagihan_id)
    data["tagihan"] = tagihan
    data["form"] = TagihanSiswaForm(instance=tagihan)
    if request.method == "POST":
        form = TagihanSiswaForm(request.POST or None, instance=tagihan)
        if form.is_valid():
            form.save()
            return redirect("admin_tagihan_detail", tagihan_id=tagihan_id)
    return render(request, "sekolah/web-admin/admin-tagihan-update.html", data)


@login_required
def admin_tagihan_hapus(request, tagihan_id):
    data = {}
    tagihan = TagihanSiswa.objects.get(pk=tagihan_id)
    if request.POST.get("confirm-delete"):
        tagihan.delete()
    return redirect("admin_tagihan")


# guru
@login_required
def admin_guru(request):
    data = {}
    list_guru = Guru.objects.filter(Q(status_guru = 'lepas') | Q(status_guru = 'tetap'))
    if request.GET.get('filter'):
        list_guru = Guru.objects.filter(status_guru=request.GET.get('filter'))
    data["list_guru"] = list_guru.order_by("nik")
    return render(request, "sekolah/web-admin/admin-guru.html", data)


@login_required
def admin_guru_add(request):
    data = {}
    if request.method == "POST":
        form = GuruForm(request.POST, request.FILES)
        if form.is_valid():
            UserModel = get_user_model()
            guru_username = int(time.time())
            guru_f_name = request.POST["nama_depan"]
            guru_l_name = request.POST["nama_belakang"]
            guru_email = "siswa@students.bunayya-school.sch.id"
            user = UserModel.objects.create_user(
                username=guru_username,
                email=guru_email,
                password="p455w0rd",
                first_name=guru_f_name,
                last_name=guru_l_name,
            )
            guru = Guru.objects.create(
                user=user,
                gelar=form.cleaned_data["gelar"],
                pas_photo=form.cleaned_data["pas_photo"],
                bio=form.cleaned_data["bio"],
                nik=form.cleaned_data["nik"],
                alamat=form.cleaned_data["alamat"],
                tanggal_lahir=form.cleaned_data["tanggal_lahir"],
                status_guru=form.cleaned_data["status_guru"],
            )

        return redirect("admin_guru")
    data["form"] = GuruForm()
    return render(request, "sekolah/web-admin/admin-guru-add.html", data)


@login_required
def admin_guru_detail(request, guru_id):
    data = {}
    data["guru"] = Guru.objects.get(pk=guru_id)
    return render(request, "sekolah/web-admin/admin-guru-detail.html", data)


@login_required
def admin_guru_update(request, guru_id):
    data = {}
    guru = Guru.objects.get(pk=guru_id)
    data["guru"] = guru
    data["form"] = GuruForm(instance=guru)
    if request.method == "POST":
        form = GuruForm(request.POST or None, instance=guru)
        if form.is_valid():
            guru_f_name = request.POST["nama_depan"]
            guru_l_name = request.POST["nama_belakang"]
            user = guru.user
            user.first_name = guru_f_name
            user.last_name = guru_l_name
            user.save()
            form.save()
            return redirect("admin_guru_detail", guru_id=guru_id)
    return render(request, "sekolah/web-admin/admin-guru-update.html", data)


@login_required
def admin_guru_hapus(request, guru_id):
    data = {}
    guru = Guru.objects.get(pk=guru_id)
    guru_user = guru.user
    if request.POST.get("confirm-delete"):
        guru_user.delete()
        guru.delete()
    return redirect("admin_guru")


# prestasi
@login_required
def admin_prestasi(request):
    data = {}
    data["list_tahun"] = TahunPelajaran.objects.all()
    data["list_prestasi"] = Prestasi.objects.all().order_by(
        "-tahun_ajaran", "-tingkat_prestasi", "ranking_prestasi"
    )
    return render(request, "sekolah/web-admin/admin-prestasi.html", data)


@login_required
def admin_prestasi_add(request):
    data = {}
    if request.method == "POST":
        form = PrestasiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("admin_prestasi")
    data["form"] = PrestasiForm()
    return render(request, "sekolah/web-admin/admin-prestasi-add.html", data)


@login_required
def admin_prestasi_detail(request, prestasi_id):
    data = {}
    data["prestasi"] = Prestasi.objects.get(pk=prestasi_id)
    return render(request, "sekolah/web-admin/admin-prestasi-detail.html", data)


@login_required
def admin_prestasi_update(request, prestasi_id):
    data = {}
    prestasi = Prestasi.objects.get(pk=prestasi_id)
    data["prestasi"] = prestasi
    data["form"] = PrestasiForm(instance=prestasi)
    if request.method == "POST":
        form = PrestasiForm(request.POST or None, instance=prestasi)
        if form.is_valid():
            form.save()
            return redirect("admin_prestasi_detail", prestasi_id=prestasi_id)
    return render(request, "sekolah/web-admin/admin-prestasi-update.html", data)


@login_required
def admin_prestasi_hapus(request, prestasi_id):
    data = {}
    prestasi = Prestasi.objects.get(pk=prestasi_id)
    if request.POST.get("confirm-delete"):
        prestasi.delete()
    return redirect("admin_prestasi")


# bank data
@login_required
def admin_bank_data(request):
    data = {}
    return render(request, "sekolah/web-admin/admin-bank-data.html", data)


# mata pelajaran
@login_required
def admin_kelas(request):
    data = {}
    data["list_tahun"] = TahunPelajaran.objects.all()
    list_kelas = Kelas.objects.all()
    list_wali_kelas = [WaliKelas.objects.get(kelas=kelas) for kelas in list_kelas]
    data["list_kelas"] = zip(list_kelas, list_wali_kelas)
    return render(request, "sekolah/web-admin/admin-kelas.html", data)


@login_required
def admin_kelas_siswa(request, kelas_id):
    data = {}
    kelas = Kelas.objects.get(pk=kelas_id)
    if request.POST.get("confirm-add-siswa"):
        siswa = Siswa.objects.get(id=request.POST["id-siswa"])
        kelas.siswa.add(siswa)
        kelas.save()
    return redirect("admin_kelas_detail", kelas_id=kelas_id)


@login_required
def admin_kelas_wali(request, kelas_id):
    data = {}
    kelas = Kelas.objects.get(pk=kelas_id)
    if request.POST.get("confirm-update-wali"):
        guru = Guru.objects.get(id=request.POST["id-guru"])
        try:
            wali_kelas = WaliKelas.objects.get(kelas=kelas)
            wali_kelas.guru = guru
            wali_kelas.save()
        except WaliKelas.DoesNotExist:
            wali_kelas = WaliKelas.objects.create(kelas=kelas, guru=guru)
    return redirect("admin_kelas_detail", kelas_id=kelas_id)


@login_required
def admin_kelas_detail(request, kelas_id):
    data = {}
    data["kelas"] = Kelas.objects.get(pk=kelas_id)
    data["list_siswa"] = [
        f"{siswa}, {siswa.tanggal_lahir} - {siswa.alamat}#id#{siswa.id}"
        for siswa in Siswa.objects.all()
    ]
    data["list_guru"] = [
        f"{guru}, {guru.tanggal_lahir} - {guru.alamat}#id#{guru.id}"
        for guru in Guru.objects.all()
    ]
    try:
        data["wali_kelas"] = WaliKelas.objects.get(kelas=data["kelas"].id)
    except WaliKelas.DoesNotExist:
        data["wali_kelas"] = None
    return render(request, "sekolah/web-admin/admin-kelas-detail.html", data)


@login_required
def admin_kelas_add(request):
    data = {}
    if request.method == "POST":
        form = KelasForm(request.POST)
        if form.is_valid():
            kelas = form.save()
            return redirect("admin_kelas_detail", kelas_id=kelas.id)
    data["form"] = KelasForm()
    return render(request, "sekolah/web-admin/admin-kelas-add.html", data)


@login_required
def admin_kelas_update(request, kelas_id):
    data = {}
    kelas = Kelas.objects.get(pk=kelas_id)
    data["kelas"] = kelas
    data["form"] = KelasForm(instance=kelas)
    if request.method == "POST":
        form = KelasForm(request.POST or None, instance=kelas)
        if form.is_valid():
            form.save()
            return redirect("admin_kelas_detail", kelas_id=kelas_id)
    return render(request, "sekolah/web-admin/admin-kelas-update.html", data)


@login_required
def admin_kelas_hapus(request, kelas_id):
    data = {}
    kelas = Kelas.objects.get(pk=kelas_id)
    if request.POST.get("confirm-delete"):
        kelas.delete()
    return redirect("admin_kelas")


# mata pelajaran
@login_required
def admin_mapel(request):
    data = {}
    data["list_tahun"] = TahunPelajaran.objects.all()
    if request.user.is_staff:
        data["list_mapel"] = MataPelajaran.objects.all()
    else:
        data["list_mapel"] = MataPelajaran.objects.filter(
            guru_pengampu__user=request.user
        )
    return render(request, "sekolah/web-admin/admin-mapel.html", data)


@login_required
def admin_mapel_detail(request, mapel_id):
    data = {}
    data["mapel"] = MataPelajaran.objects.get(pk=mapel_id)
    return render(request, "sekolah/web-admin/admin-mapel-detail.html", data)


@login_required
def admin_mapel_add(request):
    data = {}
    if request.method == "POST":
        form = MapelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("admin_mapel")
    data["form"] = MapelForm()
    return render(request, "sekolah/web-admin/admin-mapel-add.html", data)


@login_required
def admin_mapel_update(request, mapel_id):
    data = {}
    mapel = MataPelajaran.objects.get(pk=mapel_id)
    data["mapel"] = mapel
    data["form"] = MapelForm(instance=mapel)
    if request.method == "POST":
        form = MapelForm(request.POST or None, instance=mapel)
        if form.is_valid():
            form.save()
            return redirect("admin_mapel_detail", mapel_id=mapel_id)
    return render(request, "sekolah/web-admin/admin-mapel-update.html", data)


@login_required
def admin_mapel_hapus(request, mapel_id):
    data = {}
    mapel = MataPelajaran.objects.get(pk=mapel_id)
    if request.POST.get("confirm-delete"):
        mapel.delete()
    return redirect("admin_mapel")


@login_required
def admin_mapel_nilai_import(request, mapel_id):
    data = {}
    mapel = MataPelajaran.objects.get(pk=mapel_id)
    data["mapel"] = MataPelajaran.objects.get(pk=mapel_id)
    if request.POST and request.FILES['file-nilai']:
        filehandle = request.FILES.get('file-nilai')
        # To open Workbook 
        wb = xlrd.open_workbook(file_contents=filehandle.read(), on_demand = True)
        sheet = wb.sheet_by_index(0) 

        list_nilai = []
        list_nilai.append(sheet.cell_value(1, 0))
        for baris in range(3, sheet.nrows):
            siswa = {}
            siswa["id"] = sheet.cell_value(baris, 0)
            siswa["angka1"] = sheet.cell_value(baris, 3)
            siswa["huruf1"] = sheet.cell_value(baris, 4)
            siswa["deskr1"] = sheet.cell_value(baris, 5)
            siswa["angka2"] = sheet.cell_value(baris, 6)
            siswa["huruf2"] = sheet.cell_value(baris, 7)
            siswa["deskr2"] = sheet.cell_value(baris, 8)
            list_nilai.append(siswa)
        for nilai in list_nilai[1:]:
            mapel = MataPelajaran.objects.get(pk=list_nilai[0])
            siswa = Siswa.objects.get(pk=nilai['id'])
            try:
                nilai_obj = NilaiMapel.objects.get(mata_pelajaran=mapel, siswa=siswa)
                nilai_obj.nilai_angka_1 = nilai['angka1']
                nilai_obj.nilai_angka_2 = nilai['angka2']
                nilai_obj.nilai_huruf_1 = nilai['huruf1']
                nilai_obj.nilai_huruf_2 = nilai['huruf2']
                nilai_obj.deskripsi_1 = nilai['deskr1']
                nilai_obj.deskripsi_2 = nilai['deskr2']
                nilai_obj.save()
            except NilaiMapel.DoesNotExist:
                NilaiMapel.objects.create(
                    mata_pelajaran=mapel,
                    siswa=siswa,
                    nilai_angka_1=nilai['angka1'],
                    nilai_angka_2=nilai['angka2'],
                    nilai_huruf_1=nilai['huruf1'],
                    nilai_huruf_2=nilai['huruf2'],
                    deskripsi_1=nilai['deskr1'],
                    deskripsi_2=nilai['deskr2'],
                )
        wb.release_resources()
        del wb
    return redirect("admin_mapel_detail", mapel_id=mapel_id)


@login_required
def admin_mapel_nilai_template(request, mapel_id):
    mapel = MataPelajaran.objects.get(pk=mapel_id)
    nama_mapel = mapel.nama.lower().replace(' ', '-')
    kelas = mapel.kelas.nama.split(":")[0].strip()
    kelas_slug = kelas.replace(' ', '-')
    # create our spreadsheet.  I will create it in memory with a StringIO
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    cell_format = workbook.add_format({'align':'center'})
    cell_format.set_bold()
    cell_center = workbook.add_format({'align':'center'})
    cell_left = workbook.add_format({'align':'left'})
    cell_white = workbook.add_format({'font_color': 'white'})
    worksheet.set_column(0, 1, 5)
    worksheet.set_column(1, 1, 30)
    worksheet.set_column(5, 5, 50)
    worksheet.set_column(8, 8, 50)
    worksheet.merge_range('A1:I1', f"Pelajaran: {mapel.nama} {kelas} ({mapel.get_guru()})", cell_format)
    worksheet.write(f"A2", str(mapel.id), cell_white)
    worksheet.write(f"A3", "No", cell_format)
    worksheet.write(f"B3", "Nama Siswa", cell_format)
    worksheet.write(f"C3", "Kelas", cell_format)
    worksheet.write(f"D3", "Angka", cell_format)
    worksheet.write(f"E3", "Huruf", cell_format)
    worksheet.write(f"F3", "Deskripsi", cell_format)
    worksheet.write(f"G3", "Angka", cell_format)
    worksheet.write(f"H3", "Huruf", cell_format)
    worksheet.write(f"I3", "Deskripsi", cell_format)
    list_siswa = mapel.nilaimapel_set.all().order_by('-siswa')
    if not list_siswa:
        list_siswa = mapel.kelas.siswa.all().order_by('-user')
        for idx, siswa in enumerate(list_siswa, start=4):
            worksheet.write(f"A{idx}", f"{siswa.id}", cell_center)
            worksheet.write(f"B{idx}", siswa.user.get_full_name())
            worksheet.write(f"C{idx}", kelas, cell_center)
            worksheet.write(f"D{idx}", '', cell_center)
            worksheet.write(f"E{idx}", '', cell_center)
            worksheet.write(f"F{idx}", '', cell_left)
            worksheet.write(f"G{idx}", '', cell_center)
            worksheet.write(f"H{idx}", '', cell_center)
            worksheet.write(f"I{idx}", '', cell_left)
            worksheet.write(f"J{idx}", '', cell_left)
    else:
        for idx, nilai in enumerate(list_siswa, start=4):
            worksheet.write(f"A{idx}", f"{nilai.siswa.id}", cell_center)
            worksheet.write(f"B{idx}", nilai.siswa.user.get_full_name())
            worksheet.write(f"C{idx}", kelas, cell_center)
            worksheet.write(f"D{idx}", nilai.nilai_angka_1, cell_center)
            worksheet.write(f"E{idx}", nilai.nilai_huruf_1, cell_center)
            worksheet.write(f"F{idx}", nilai.deskripsi_1, cell_left)
            worksheet.write(f"G{idx}", nilai.nilai_angka_2, cell_center)
            worksheet.write(f"H{idx}", nilai.nilai_huruf_2, cell_center)
            worksheet.write(f"I{idx}", nilai.deskripsi_2, cell_left)
            worksheet.write(f"J{idx}", '', cell_left)
    workbook.close()

    # create a response
    response = HttpResponse(content_type="application/vnd.ms-excel")

    # tell the browser what the file is named
    response["Content-Disposition"] = f'attachment;filename="{nama_mapel}-{kelas_slug.lower()}.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    return response
