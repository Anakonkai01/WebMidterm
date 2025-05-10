from flask import request
from flask_restful import Resource
from app.models import Product
from app.schemas import product_schema, products_schema
from app import db
from marshmallow import ValidationError


class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return products_schema.dump(products), 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            # Validate và deserialize input
            data = product_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422 # Unprocessable Entity

        # Tạo đối tượng Product từ dữ liệu đã được load (nếu load_instance=True)
        # Hoặc new_product = Product(**data) nếu data là dict
        new_product = data # Vì load_instance=True, data đã là một đối tượng Product

        db.session.add(new_product)
        db.session.commit()
        return product_schema.dump(new_product), 201


class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id, description=f"Product with ID {product_id} not found.")
        return product_schema.dump(product), 200

    def put(self, product_id):
        product = Product.query.get_or_404(product_id, description=f"Product with ID {product_id} not found.")
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            # Validate và cập nhật instance
            # product_schema.load(json_data, instance=product, partial=True)
            # Marshmallow 3.x: instance parameter is deprecated in load.
            # Instead, pass instance to the Schema constructor.
            # Hoặc cập nhật thủ công các trường:
            updated_product = product_schema.load(json_data, partial=True) # Load dữ liệu mới, cho phép thiếu trường

            # Cập nhật các trường của product từ updated_product (là dict hoặc object tùy schema)
            for key, value in product_schema.dump(updated_product).items(): # dump để lấy dict an toàn
                if hasattr(product, key):
                    setattr(product, key, value)

        except ValidationError as err:
            return err.messages, 422

        db.session.commit()
        return product_schema.dump(product), 200

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id, description=f"Product with ID {product_id} not found.")
        db.session.delete(product)
        db.session.commit()
        return {'message': f'Product with ID {product_id} deleted successfully.'}, 200