# Generated by Django 3.2 on 2023-06-02 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('jenis_kelamin', models.CharField(choices=[['Laki-Laki', 'l'], ['Perempuan', 'p']], max_length=30)),
                ('alamat', models.TextField()),
                ('telp', models.CharField(max_length=15)),
                ('spesialis', models.CharField(max_length=50)),
                ('pendidikan', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Siswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100, verbose_name='Nama Siswa')),
                ('tempat_lahir', models.CharField(max_length=30, verbose_name='Tempat Lahir')),
                ('tgl_lahir', models.DateField(verbose_name='Tanggal Lahir')),
                ('jenis_kelamin', models.CharField(choices=[['Laki-Laki', 'l'], ['Perempuan', 'p']], max_length=10)),
                ('alamat', models.TextField()),
                ('kota', models.CharField(max_length=30)),
                ('telp', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('kelas', models.CharField(max_length=15)),
                ('angkatan', models.DateField(max_length=15)),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akademik.guru')),
            ],
        ),
        migrations.CreateModel(
            name='Pelajaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='akademik.guru')),
            ],
        ),
    ]