# Generated by Django 3.2 on 2023-06-02 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('akademik', '0002_auto_20230603_0032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Biaya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_biaya', models.CharField(max_length=30)),
                ('tahun_akademik', models.DateField()),
                ('biaya', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sisa', models.IntegerField()),
                ('potongan', models.IntegerField()),
                ('biaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keuangan.biaya')),
                ('nama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akademik.siswa')),
            ],
        ),
        migrations.CreateModel(
            name='DetailTransaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgl_transaksi', models.DateTimeField()),
                ('angsuran', models.IntegerField()),
                ('jumlah_angsuran', models.IntegerField()),
                ('biaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keuangan.biaya')),
                ('nama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akademik.siswa')),
            ],
        ),
    ]
