# from datetime import date
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
# from api.models import Employee, WorkInformation, PersonalInformation
# from utils import pbdkf2_sha256


# def add_user():
#     # Thêm các bản ghi cho bảng auth_user
#     users_data = [
#         {
#             "id": 9,
#             "username": "act_user_9",
#             "email": "act_user_9@gmail.com",
#             "password": "Matkhauhople1",
#         }
#     ]
#     for user_data in users_data:
#         user_data["password"] = pbdkf2_sha256.pbkdf2_sha256(user_data["password"])
#         user_data["date_joined"] = date.today()
#         try:
#             user = User.objects.get(username="act_user_9")
#             user.delete()
#             print("User đã được xóa.")
#         except User.DoesNotExist:
#             print("User không tồn tại.")
        
#         User.objects.create(**user_data)

# add_user()
