from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import employee_detail, files, employee_list, health_check, me, overview

app_name = "api"

urlpatterns = [
    # Health check
    path("health_check/", health_check, name="health_check"),
    # JWT
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
    path("me/", me, name="me"),
    # Employe
    path("employees/", employee_list, name="employee_list"),
    path("employees/<str:code>/", employee_detail, name="employee_detail"),
    # Dashboard
    path("overview/", overview, name="overview"),
    # Files
    path("files/", files, name="files"),
]
