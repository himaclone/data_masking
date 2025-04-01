from django.urls import path
# from rest_framework_simplejwt import views as jwt_views

from . import views
# from .views import upload_view

# app_name = "api"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('upload/', views.upload_view, name='upload'),
    path('employees/<str:code>/', views.employee_detail_view, name='employee'),
]
