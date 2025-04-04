# Generated by Django 5.0.3 on 2025-04-02 11:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted_at", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "created_at",
                    models.CharField(default="02-04-2025 18:24:40", max_length=255),
                ),
                (
                    "updated_at",
                    models.CharField(default="02-04-2025 18:24:40", max_length=255),
                ),
                ("code", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
                ("gender", models.CharField(default="male", max_length=255)),
                ("date_of_birth", models.CharField(max_length=255)),
                (
                    "probationary_start_date",
                    models.CharField(max_length=255, null=True),
                ),
                ("probationary_end_date", models.CharField(max_length=255, null=True)),
                ("official_start_date", models.CharField(max_length=255)),
                ("tax_code", models.CharField(max_length=255)),
                ("social_insurance_code", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                ("level", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=255)),
                ("citizen_identification_code", models.CharField(max_length=255)),
                ("personal_email", models.CharField(max_length=255)),
                ("birthplace", models.CharField(max_length=255)),
                ("current_address", models.CharField(max_length=255)),
                ("permanent_address", models.CharField(max_length=255)),
                ("bank_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "bank_account_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("education", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "graduation_year",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Employees information",
                "db_table": "employees_information",
            },
        ),
        migrations.CreateModel(
            name="FileUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("deleted_at", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "created_at",
                    models.CharField(default="02-04-2025 18:24:40", max_length=255),
                ),
                (
                    "updated_at",
                    models.CharField(default="02-04-2025 18:24:40", max_length=255),
                ),
                ("file", models.FileField(upload_to="files")),
                ("is_encrypted", models.BooleanField(blank=True, default=False)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="api.employee",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Files Uploading",
                "db_table": "files_uploading",
            },
        ),
    ]
