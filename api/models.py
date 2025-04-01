from datetime import date, datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class BaseModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BaseModelManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        ordering = ("-created_at",)
        abstract = True


class Employee(BaseModel):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name_plural = "Employees"
        db_table = "employees"


class WorkInformation(BaseModel):
    TYPE_CHOICES = (
        ("sse", "Server-side Engineer"),
        ("cse", "Client-side Engineer"),
        ("qa", "Quality assurance"),
        ("pm", "Project manager"),
    )
    LEVEL_CHOICES = (
        ("jr", "Junior"),
        ("mid", "Middle"),
        ("sr", "Senior"),
        ("ex", "Expert"),
    )

    employee = models.OneToOneField(
        to=Employee,
        on_delete=models.CASCADE,
        related_name="work_information",
    )
    probationary_start_date = models.DateField(null=True)
    probationary_end_date = models.DateField(null=True)
    official_start_date = models.DateField(null=False)
    tax_code = models.CharField(max_length=255)
    social_insurance_code = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.employee.code

    class Meta:
        verbose_name_plural = "Work Informations"
        db_table = "work_informations"


class PersonalInformation(BaseModel):
    employee = models.OneToOneField(
        to=Employee,
        on_delete=models.CASCADE,
        related_name="personal_information",
    )
    phone_number = models.CharField(max_length=10)
    citizen_identification_code = models.CharField(max_length=20)
    personal_email = models.EmailField(max_length=254)
    birthplace = models.CharField(max_length=255)
    current_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_account_number = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    graduation_year = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(date.today().year),
        ],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.employee.code

    class Meta:
        verbose_name_plural = "Personal Informations"
        db_table = "personal_informations"


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
        verbose_name_plural = "File Uploads"
        db_table = "file_uploads"
