from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django import forms
import requests

from rest_framework_simplejwt.tokens import RefreshToken

API_BASE_URL = 'http://localhost:8000/api/v1/'

def get_tokens_for_user(user):
    # Tạo token cho người dùng
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Hàm để lấy dữ liệu từ API
def get_data(endpoint):
    url = f"{API_BASE_URL}{endpoint}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Form for user login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# Form for file upload
class UploadForm(forms.Form):
    file = forms.FileField()

# View for login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                tokens = get_tokens_for_user(user)
                request.session['access_token'] = tokens['access']  # Lưu access token vào session
                request.session['refresh_token'] = tokens['refresh']  # Lưu refresh token (tùy chọn)
                
                messages.success(request, "Đăng nhập thành công!")
                return redirect('home')
            else:
                return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# View for file upload
@login_required
def upload_view(request):

    employee_id = request.user.employee.id

    if request.method == 'POST':
        # data = request.data
        # data["employee"] = employee_id
        # serializer = FileUploadSerializer(data=data)

        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            with open(f'/tmp/{file.name}', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return HttpResponse('File uploaded successfully')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

# View for file home
@login_required
def home_view(request):
    token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}employees/", headers=headers)
    employees = response.json() if response.status_code == 200 else []

    return render(request, "home.html", {"employees": employees})


# @login_required
def employee_detail_view(request, code):
    token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}employees/{code}/", headers=headers)
    employee = response.json() if response.status_code == 200 else []

    return render(request, "employee_detail.html", {"employee": employee})
