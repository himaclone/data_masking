# demo-data-masking-be
Đây là server của dự án Data Masking phục vụ môn học **Cơ sở an toàn và bảo mật thông tin**

# Run Project on local machine
Các phần mềm cần có: ***make***, ***docker***.

Để chạy dự án ở local machine, cần thực hiện các bước sau:

- B1: Copy file env
```bash
make copy-env
```
- B2: Build image
```bash
make build
```
- B3: Chạy server (Các lần chạy sau chỉ cần bước này)
```bash
make start
```
- B4: Migrate database
```bash
make run cmd="python manage.py migrate"
```
- B5: Thêm data mẫu (Optional)
```bash
make add-sample-data
```
- B6: Tạo tài khoản superuser để truy cập http://localhost:8000/admin
```bash
make run cmd="python manage.py createsuperuser"
```
