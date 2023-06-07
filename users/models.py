from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class User(AbstractUser):
    REQUESTED_ACCOUNT_TYPE_CHOICES = (
        ('subscriber', 'Subscriber'),
        ('student', 'Siswa'),
        ('teacher', 'Guru'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
    )

    STATUS = (
        ('n', 'Pengajuan Tidak Disetujui'),
        ('p', 'Menunggu Persetujuan'),
        ('d', 'Pengajuan Ditolak'),
        ('a', 'Pengajuan Diterima')
    )

    approval_status = models.CharField(
        max_length=2, choices=STATUS, default='n')
    employee_or_student_id = models.CharField(
        max_length=10, null=True, blank=True)
    requested_role = models.CharField(
        max_length=15, choices=REQUESTED_ACCOUNT_TYPE_CHOICES, default=REQUESTED_ACCOUNT_TYPE_CHOICES[0][0])
    approval_note = models.TextField(blank=True, null=True)


class CustomGroup(Group):
    group_creator = models.ForeignKey('User', on_delete=models.CASCADE)

    def display_group(self):
        return f'{self.name} dibuat oleh {self.group_creator}'


class SocialLink(models.Model):
    user_profile = models.ForeignKey(
        'CommonUserProfile', on_delete=models.CASCADE)
    media_name = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.media_name


class CommonUserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(
        upload_to='profile-picture', blank=True, null=True)
    cover_picture = models.ImageField(
        upload_to='cover-picture', blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True, null=True)
    show_headline_in_bio = models.BooleanField(
        help_text="I want to use this as my bio", default=False)
    summary = RichTextUploadingField(help_text='Ringkasan profilmu')
    social_link = models.ManyToManyField(
        SocialLink, related_name='social_links', blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user}'s profile"
