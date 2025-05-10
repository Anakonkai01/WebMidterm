# run.py
import os
from app import create_app # Import hàm factory create_app từ package app

# Lấy tên cấu hình từ biến môi trường FLASK_ENV.
config_name = os.getenv('FLASK_ENV', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()