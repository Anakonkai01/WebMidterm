import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
api = Api() # Khởi tạo Api của Flask-RESTful

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Đảm bảo thư mục instance tồn tại
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Đăng ký API resources
    from app.resources import ProductListResource, ProductResource # Import sau khi 'api' được tạo
    api.add_resource(ProductListResource, '/api/products')
    api.add_resource(ProductResource, '/api/products/<int:product_id>')

    api.init_app(app) # Phải gọi init_app cho Api sau khi add_resource nếu bạn khởi tạo Api() trước

    # Import models ở đây để Flask-Migrate có thể nhận diện được trong ngữ cảnh ứng dụng
    from app import models

    return app