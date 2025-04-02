from django.contrib.auth.models import User
from api.models import Employee

def reset_data():
    # Xóa các bản ghi từ bảng PersonalInformation
    # PersonalInformation.objects.all().delete()

    # Xóa các bản ghi từ bảng WorkInformation
    # WorkInformation.objects.all().delete()

    # Xóa các bản ghi từ bảng Employee
    Employee.objects.all().delete()

    # Xóa các bản ghi từ bảng User (trừ admin)
    User.objects.exclude(username='admin').delete()

    print("Đã xóa hết dữ liệu mẫu và reset về trạng thái ban đầu.")


reset_data()
