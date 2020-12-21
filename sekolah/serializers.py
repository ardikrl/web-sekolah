from rest_framework import serializers

from .models import TagihanSiswa


class TagihanSiswaSerializer(serializers.ModelSerializer):
    siswa = serializers.CharField(source='siswa.user.get_full_name', read_only=True)
    nis = serializers.CharField(source='siswa.nis_siswa', read_only=True)
    nisn = serializers.CharField(source='siswa.nisn_siswa', read_only=True)
    kelas = serializers.CharField(source='siswa.kelas', read_only=True)
    penerima = serializers.CharField(source='penerima.user.get_full_name', read_only=True)
    kategori = serializers.CharField(source='kategori_verbose', read_only=True)
    status = serializers.CharField(source='status_verbose', read_only=True)

    class Meta:
        model = TagihanSiswa
        fields = (
            "siswa",
            "nis",
            "nisn",
            "kelas",
            "penerima",
            "keterangan",
            "kategori",
            "status",
            "tanggal_tagihan",
            "tanggal_bayar",
            "tagihan",
            "created_at",
            "updated_at",
        )
