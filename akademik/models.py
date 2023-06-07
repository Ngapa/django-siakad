from model_utils.models import TimeStampedModel

from django.db import models, OperationalError
from django.conf import settings
from django.urls import reverse

from teacher.models import Teacher


class AcademicSession(TimeStampedModel):
    year = models.PositiveIntegerField(unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'{self.year} - {self.year + 1}'


class Semester(TimeStampedModel):
    number = models.PositiveIntegerField(unique=True)
    guide = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, default=None, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['number',]

    def __str__(self):
        return str(self.number)


class Subject(TimeStampedModel):
    name = models.CharField(max_length=50)
    subject_code = models.PositiveIntegerField(unique=True)
    book_cover = models.ImageField(
        upload_to='subject/', default='subject/book_cover.jpg')
    instructor = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING, null=True, blank=True)
    theory_marks = models.PositiveIntegerField(blank=True, null=True)
    practical_marks = models.PositiveIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'{self.name} ({self.subject_code})'


class Batch(TimeStampedModel):
    year = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    number = models.PositiveIntegerField("Batch Number")

    class Meta:
        verbose_name_plural = 'Batches'
        unique_together = ['year', 'number']

    def __str__(self):
        return f'Batch {self.number} ({self.year})'


class TempSerialID(TimeStampedModel):
    student = models.OneToOneField(
        'students.Student', on_delete=models.CASCADE, related_name='student_serial')
    year = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    serial = models.CharField(max_length=50, blank=True)

    # class Meta:
    #     unique_together = ['department', 'year']

    def __str__(self):
        return self.serial

    def save(self, *args, **kwargs):
        if self.student.admission_student.admitted:
            super().save(*args, **kwargs)
        else:
            raise OperationalError(
                'Please check if student is admitted or not.')

    def get_serial(self):
        # Get current year last two digit
        yf = str(self.student.ac_session)[-2:]
        # Get current batch of student's department
        bn = self.student.batch.number
        # Get admission serial of student by department
        syl = self.serial

        # return something like: 21-15-666-15
        return f'{yf}-{bn}-{syl}'
