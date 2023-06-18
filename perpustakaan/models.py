from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings


class Genre(TimeStampedModel):
    name = models.CharField(
        max_length=150, help_text='Masukan genre buku (contoh: Fiksi Ilmiah, Sastra Indonesia, Sejarah, dll)')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name


class Book (TimeStampedModel):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    summary = models.TextField(
        max_length=1000, help_text='Masukan deskripsi singkat dari buku ini')
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Karakter <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text='Pilih genre dari buku ini')
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField()
    avalaible_copies = models.IntegerField()
    pic = models.ImageField(blank=True, null=True, upload_to='book_image')

    def __str__(self):
        return self.title
