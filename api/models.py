from datetime import date, datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class BaseModel(models.Model):
    deleted_at = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.CharField(max_length=255, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    updated_at = models.CharField(max_length=255, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    objects = BaseModelManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        ordering = ("-created_at",)
        abstract = True


class Employee(BaseModel):
    # GENDER_CHOICES = [
    #     ("male", "Male"),
    #     ("female", "Female"),
    #     ("other", "Other"),
    # ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, default="male")
    date_of_birth = models.CharField(max_length=255)

    #work
    # TYPE_CHOICES = (
    #     ("sse", "Server-side Engineer"),
    #     ("cse", "Client-side Engineer"),
    #     ("qa", "Quality assurance"),
    #     ("pm", "Project manager"),
    # )
    # LEVEL_CHOICES = (
    #     ("jr", "Junior"),
    #     ("mid", "Middle"),
    #     ("sr", "Senior"),
    #     ("ex", "Expert"),
    # )

    probationary_start_date = models.CharField(max_length=255, null=True)
    probationary_end_date = models.CharField(max_length=255, null=True)
    official_start_date = models.CharField(max_length=255, null=False)
    tax_code = models.CharField(max_length=255)
    social_insurance_code = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    level = models.CharField(max_length=255)

    #personal
    phone_number = models.CharField(max_length=255)
    citizen_identification_code = models.CharField(max_length=255)
    personal_email = models.CharField(max_length=255)
    birthplace = models.CharField(max_length=255)
    current_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    graduation_year = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name_plural = "Employees information"
        db_table = "employees_information"

class FileUpload(BaseModel):
    employee = models.ForeignKey(
        to=Employee,
        on_delete=models.CASCADE,
        related_name="files",
    )
    file = models.FileField(upload_to="files")
    is_encrypted = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name_plural = "Files Uploading"
        db_table = "files_uploading"
