from django.contrib import admin

from .models import Employee, FileUpload

admin.site.register(Employee)
admin.site.register(FileUpload)
# admin.site.register(WorkInformation)
# admin.site.register(PersonalInformation)
