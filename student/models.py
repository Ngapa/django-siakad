from datetime import datetime

from model_utils.models import TimeStampedModel

from django.conf import settings
from django.db import models, OperationalError, IntegrityError, transaction




class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_alumni = False,
            is_droped = False
        )
        
class AlumniManager(models.Manager):
    def get_queryset(self):
        return super().get_queyset().filter(
            is_alumni = True
        )
        
class StudentBase(TimeStampedModel):
    name = models.CharField("Nama Lengkap", max_length=100)
    photo = models.ImageField(upload_to='students/applicants/', null=True, blank=True)
    fath_name = models.CharField("Nama Ayah", max_length=100)
    moth_name = models.CharField("Nama Ibu", max_length=100)
    city = models.CharField("Kota", max_length=50)
    address = models.TextField("Alamat")
    phone_number = models.CharField("Nomor Telepon", max_length=15)
    guardian_phone_number = models.CharField("Nomor Telepon Wali", max_length=15)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name
        
class CounselingComment(TimeStampedModel):
    conselor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    registrant_student = models.ForeignKey('AdmissionStudent', on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=255)
    
    def __str__(self):
        date = self.created.strftime("%d %B %Y")
        return self.comment
    
    class Meta:
        ordering = ["-created", ]
        
class AdmissionStudent(StudentBase):
    EXAM_NAMES = (
        ("UTS", "Ujian Tengah Semester"),
        ("UAS", "Ujian Akhir Semester"),
        ("tugas", "Tugas"),
    )
    
    counseling_by = models.ForeignKey(Teacher, related_name='counselor', on_delete=models.CASCADE, null=True)
    counsel_comment = models.ManyToManyField(CounselingComment, blank=True)
    exam_name = models.CharField("Exam Name", choices=EXAM_NAMES, max_length=10)
    passing_year = models.CharField(max_length=4)
    group = models.CharField(max_length=15)
    gpa = models.DecimalField(decimal_places=2, max_digits=4)
    marksheet_image = models.ImageField("Upload your Marksheet", upload_to='student/applicant/marksheets/',null=True, blank=True)
    admission_policy_agreement = models.BooleanField(default=False)
    admitted = models.BooleanField(default=False)
    admission_date = models.DateField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    migration_status = models.CharField(max_length=255, blank=True, null=True)
    rejected = models.BooleanField(default=False)
    assigned_as_student = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}"
        
class Student(TimeStampedModel):
    admission_student = models.ForeignKey(AdmissionStudent, on_delete=models.CASCADE)
    roll = models.CharField(max_length=7, unique=True, blank=True, null=True)
    registration_number = models.CharField(max_length=7, unique=True, blank=True, null=True)
    temp_serial = models.CharField(max_length=50, blank=True, null=True)
    temporary_id = models.CharField(max_length=50, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    ac_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, blank=True, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=True, null=True)
    guardian_mobile = models.CharField(max_length=15, blank=True, null=True)
    admitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    is_alumni = models.BooleanField(default=False)
    is_dropped = models.BooleanField(default=False)
    
    #manager
    objects = StudentManager()
    alumnus = AlumniManager()
    
    class Meta:
        ordering = ['semester', 'roll', 'registration_number']
    
    def __str__(self):
        return f"{self.admission_student.name} ({self.semester})"
        
    def _find_last_admitted_student_serial(self):
        item_serial_obj = TempSerialID.objects.filter(year= self.ac_session).order_by('serial').last()
        
        if item_serial_obj:
            serial_number = item_serial_obj.serial
            return int(serial_number)
        else:
            return 0
        
    def get_temp_id(self):
        year_digit = str(self.ac_session.year)[-2:]
        batch_digit = self.batch.number
        temp_serial_key = self.temp_serial
        temp_id = f'{year_digit}-{batch_digit}-{temp_serial_key}'
        
        return temp_id
        
    def save(self, *args, **kwargs):
        if not self.temp_serial or not self.temporary_id:
            last_temp_id = self._find_last_admitted_student_serial()
            current_temp_id = str(last_temp_id + 1)
            self.temp_serial  = current_temp_id
            self.temporary_id = self.get_temp_id()
            super().save(*args, **kwargs)
            try:
                with transaction.atomic():
                    temp_serial_id = TempSerialID.objects.create(student=self, year=self.ac_session, serial= current_temp_id)
                    temp_serial_id.save()
            except IntegrityError:
                pass
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        """Override delete method"""
        self.admission_student.assigned_as_student = False
        self.admission_student.save(*args, **kwargs)
        
        
class RegularStudent(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.ATUH_USER_MODEL, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.student.name} {self.semester}'