/flask_phone_shop_api  # Đổi tên thư mục dự án cho mới mẻ :)
    ├── venv/
    ├── app/
    │   ├── __init__.py             # Khởi tạo package 'app' và ứng dụng Flask (dùng create_app)
    │   ├── config.py               # Các lớp cấu hình (Development, Production, Testing)
    │   ├── models.py               # Định nghĩa các model CSDL (User, Product, Category, Order...)
    │   ├── schemas.py              # Định nghĩa các schema Marshmallow (để serialize/deserialize và validate)
    │   ├── resources/              # Thư mục chứa các resource API (Flask-RESTful)
    │   │   ├── __init__.py
    │   │   ├── auth_resource.py    # Endpoints cho /auth (register, login, refresh, logout)
    │   │   ├── user_resource.py    # Endpoints cho /users (ví dụ: lấy thông tin user, cập nhật profile)
    │   │   ├── product_resource.py # Endpoints cho /products
    │   │   ├── category_resource.py# Endpoints cho /categories (MỚI)
    │   │   └── order_resource.py   # Endpoints cho /orders (MỚI)
    │   ├── services/               # (Tùy chọn, nâng cao) Chứa business logic tách biệt
    │   │   ├── __init__.py
    │   │   └── auth_service.py
    │   │   └── product_service.py
    │   └── utils/                  # (Tùy chọn) Chứa các hàm tiện ích
    │       ├── __init__.py
    │       └── helpers.py
    ├── migrations/                 # Thư mục do Flask-Migrate tạo (sẽ giới thiệu sau)
    ├── run.py                      # File để chạy ứng dụng Flask
    ├── .env                        # File lưu trữ biến môi trường
    ├── .gitignore
    ├── requirements.txt
    └── README.md