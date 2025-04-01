from django.db.models import Case, CharField, Count, Value, When
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Employee, FileUpload, WorkInformation
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
    whens = [When(type=k, then=Value(v)) for k, v in WorkInformation.TYPE_CHOICES]
    queryset = (
        WorkInformation.objects.annotate(
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


@api_view(["GET"])
def employee_detail(request, code):
    employee = get_object_or_404(
        Employee.objects.select_related(
            "work_information",
            "personal_information",
        ),
        code=code,
    )
    if code == request.user.employee.code:
        serializer = EmployeeDetailSerializer(employee)
    else:
        serializer = MaskedEmployeeDetailSerializer(employee)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def files(request):

    employee_id = request.user.employee.id

    if request.method == "POST":
        data = request.data
        data["employee"] = employee_id
        serializer = FileUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        files = FileUpload.objects.filter(employee_id=employee_id)
        serializer = FileUploadListSerializer(files, many=True)
        return Response(serializer.data)
