from django.db import models
from akademik.models import Siswa


class Biaya(models.Model):
    jenis_biaya = models.CharField(max_length=30)
    tahun_akademik = models.DateField()
    biaya = models.IntegerField()


class Transaksi(models.Model):
    nama = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    biaya = models.ForeignKey('Biaya', on_delete=models.CASCADE)
    sisa = models.IntegerField()
    potongan = models.IntegerField()


class DetailTransaksi(models.Model):
    biaya = models.ForeignKey('Biaya', on_delete=models.CASCADE)
    nama = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    tgl_transaksi = models.DateTimeField()
    angsuran = models.IntegerField()
    jumlah_angsuran = models.IntegerField()
