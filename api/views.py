from django.db.models import Case, CharField, Count, Value, When
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import FileResponse
from utils import aes_string
import os

import utils.aes_string

from .models import Employee, FileUpload
from .serializers import (
    EmployeeDetailSerializer,
    EmployeeListSerializer,
    FileUploadSerializer,
    FileUploadListSerializer,
    MaskedEmployeeDetailSerializer,
    TypeCountSerializer,
)


@api_view(["GET"])
def health_check(_):
    return Response({"healthy": True})


@api_view(["GET"])
def me(request):
    me = Employee.objects.filter(user_id=request.user.id).first()
    serializer = EmployeeDetailSerializer(me)
    return Response(serializer.data)


@api_view(["GET"])
def overview(_):
    whens = [When(type=k, then=Value(v)) for k, v in Employee.TYPE_CHOICES]
    queryset = (
        Employee.objects.annotate(
            type_display=Case(*whens, output_field=CharField())
        )
        .values("type_display")
        .annotate(count=Count("type"))
    )
    serializer = TypeCountSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def employee_list(request):
    employees = Employee.objects.all()
    serializer = EmployeeListSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def employee_detail(request, code):
    if request.method == "POST":
        employee = get_object_or_404(
            Employee.objects.all(),
            code=code,
        )
        key = request.POST.get('key').encode("utf-8");
        serializer = MaskedEmployeeDetailSerializer(employee)

        try:
            employee.name = aes_string.aes_decrypt_string(bytes.fromhex(employee.name) ,key)
            employee.email = aes_string.aes_decrypt_string(bytes.fromhex(employee.email) ,key)
            employee.gender = aes_string.aes_decrypt_string(bytes.fromhex(employee.gender) ,key)
            employee.date_of_birth = aes_string.aes_decrypt_string(bytes.fromhex(employee.date_of_birth) ,key)
            employee.probationary_end_date = aes_string.aes_decrypt_string(bytes.fromhex(employee.probationary_end_date) ,key)
            employee.probationary_start_date = aes_string.aes_decrypt_string(bytes.fromhex(employee.probationary_start_date) ,key)
            employee.official_start_date = aes_string.aes_decrypt_string(bytes.fromhex(employee.official_start_date) ,key)
            employee.tax_code = aes_string.aes_decrypt_string(bytes.fromhex(employee.tax_code) ,key)
            employee.social_insurance_code = aes_string.aes_decrypt_string(bytes.fromhex(employee.social_insurance_code) ,key)
            employee.type = aes_string.aes_decrypt_string(bytes.fromhex(employee.type) ,key)
            employee.level = aes_string.aes_decrypt_string(bytes.fromhex(employee.level) ,key)
            employee.phone_number = aes_string.aes_decrypt_string(bytes.fromhex(employee.phone_number) ,key)
            employee.citizen_identification_code = aes_string.aes_decrypt_string(bytes.fromhex(employee.citizen_identification_code) ,key)
            employee.personal_email = aes_string.aes_decrypt_string(bytes.fromhex(employee.personal_email) ,key)
            employee.birthplace = aes_string.aes_decrypt_string(bytes.fromhex(employee.birthplace) ,key)
            employee.current_address = aes_string.aes_decrypt_string(bytes.fromhex(employee.current_address) ,key)
            employee.permanent_address = aes_string.aes_decrypt_string(bytes.fromhex(employee.permanent_address) ,key)
            employee.bank_name = aes_string.aes_decrypt_string(bytes.fromhex(employee.bank_name) ,key)
            employee.bank_account_number = aes_string.aes_decrypt_string(bytes.fromhex(employee.bank_account_number) ,key)
            employee.education = aes_string.aes_decrypt_string(bytes.fromhex(employee.education) ,key)
            employee.graduation_year = aes_string.aes_decrypt_string(bytes.fromhex(employee.graduation_year) ,key)
        except Exception as e:
            print(f"Lỗi giải mã: {e}")
            return Response(serializer.data)


        if code == request.user.employee.code:
            serializer = EmployeeDetailSerializer(employee)
        else:
            serializer = MaskedEmployeeDetailSerializer(employee)
        return Response(serializer.data)
    
    if request.method == "GET":
        employee = get_object_or_404(
            Employee.objects.all(),
            code=code,
        )
        # if code == request.user.employee.code:
        #     serializer = EmployeeDetailSerializer(employee)
        # else:
        serializer = MaskedEmployeeDetailSerializer(employee)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def files(request):

    employee_id = request.user.employee.id

    if request.method == "POST":
        data = request.data
        data["employee"] = employee_id
        is_encrypted = request.POST.get('is_encrypted') == 'true'
        if(is_encrypted):
            data["file"] = ContentFile(utils.aes_string.aes_encrypt_string(data["file"].read().decode('utf-8'), data["key"].encode('utf-8')), name=data["file"].name)
        
        serializer = FileUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # files = FileUpload.objects.filter(employee_id=employee_id)
        files = FileUpload.objects.all()

        serializer = FileUploadListSerializer(files, many=True)
        return Response(serializer.data)
    
@api_view(["POST"])
def file_download(request, id):
    
    # if request.method == "POST":
    try:
        file = get_object_or_404(
            FileUpload.objects.all(),
            id=id,
        )
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        #Kiểm tra file có tồn tại không
        if not os.path.exists(file_path):
            return Response({"error": "File not found on server"}, status=404)
        # Đọc nội dung file
        
        is_encrypted = file.is_encrypted
        # Nếu file được mã hóa, giải mã trước
        if is_encrypted:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            key = request.POST.get('key')
            if not key:
                return Response({"error": "Key is required to decrypt the file"}, status=400)
            try:
                file_content = utils.aes_string.aes_decrypt_string(file_content, key.encode("utf-8"))
            except Exception as e:
                return Response({"error": f"Decryption failed: {str(e)}"}, status=400)
        else:
            with open(file_path, 'r') as f:
                file_content = f.read()
        # Trả về file dưới dạng response tải xuống
        response = FileResponse(
            file_content,
            as_attachment=True,
            filename=file.file.name
        )
        return response
    except FileUpload.DoesNotExist:
        return Response({"error": "File not found in database"}, status=404)
