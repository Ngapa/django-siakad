from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel
from taggit.managers import TaggableManager


class Designation(TimeStampedModel):
    title = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Teacher(TimeStampedModel):
    name = models.CharField(max_length=150)
    photo = models.ImageField(
        upload_to="teacher", default="teacher/default.png")
    date_birth = models.DateField(null=True, blank=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.CASCADE, related_name='resources')
    expertise = TaggableManager(blank=True)
    mobile = models.CharField(max_length=13, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['joining_date', 'name']

    def __str__(self):
        return f'{self.name} - {self.designation}'
