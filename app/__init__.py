# app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api as FlaskRestfulApi # Đổi tên để tránh xung đột
from flask_migrate import Migrate
import os

from .config import config_by_name

# Khởi tạo extensions mà không có app instance ban đầu
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()
# Không khởi tạo FlaskRestfulApi ở đây nữa, sẽ khởi tạo bên trong create_app
migrate = Migrate()

# (Tùy chọn) Tạo một set để lưu trữ các JTI của token đã bị blacklist (cho logout)
# BLACKLISTED_JWT = set()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Khởi tạo các extensions với app instance
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db) # Khởi tạo Flask-Migrate

    # Khởi tạo Flask-RESTful API object VÀ đặt prefix ngay lúc này
    api_restful = FlaskRestfulApi(app, prefix='/api/v1')

    # Import models ở đây để Flask-Migrate có thể nhận diện được chúng
    # và để các phần khác của ứng dụng có thể import
    with app.app_context():
        from . import models # Quan trọng: import models sau khi db đã được init_app

    # Import và đăng ký các resources (API endpoints)
    from .resources.auth_resource import UserRegisterResource, UserLoginResource, TokenRefreshResource #, UserLogoutResource
    from .resources.user_resource import UserResource # , UserListResource
    from .resources.product_resource import ProductListResource, ProductResource
    from .resources.category_resource import CategoryListResource, CategoryResource
    # from .resources.order_resource import OrderListResource, OrderResource

    # Đăng ký các resource với Flask-RESTful
    api_restful.add_resource(UserRegisterResource, '/auth/register')
    api_restful.add_resource(UserLoginResource, '/auth/login')
    api_restful.add_resource(TokenRefreshResource, '/auth/refresh')
    # api_restful.add_resource(UserLogoutResource, '/auth/logout')

    api_restful.add_resource(UserResource, '/users/<int:user_id>')
    # api_restful.add_resource(UserListResource, '/users')

    api_restful.add_resource(ProductListResource, '/products')
    api_restful.add_resource(ProductResource, '/products/<int:product_id>')

    api_restful.add_resource(CategoryListResource, '/categories')
    api_restful.add_resource(CategoryResource, '/categories/<int:category_id>')

    # api_restful.add_resource(OrderListResource, '/orders')
    # api_restful.add_resource(OrderResource, '/orders/<int:order_id>')


    # (Tùy chọn) Các hàm xử lý lỗi JWT tùy chỉnh
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(message="Token has expired.", error="token_expired"), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify(message="Signature verification failed or token is invalid.", error="invalid_token", details=error_string), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify(message="Request does not contain an access token.", error="authorization_required", details=error_string), 401

    # (Tùy chọn) Callback để kiểm tra xem token có trong blacklist không
    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     jti = jwt_payload["jti"]
    #     return jti in BLACKLISTED_JWT

    # @jwt.revoked_token_loader
    # def revoked_token_callback(jwt_header, jwt_payload):
    #     return jsonify(description="The token has been revoked.", error="token_revoked"), 401

    @app.route('/') # Route gốc để kiểm tra
    def index():
        return jsonify(message="Welcome to the Flask Phone Shop API! (v1)")

    return app