from app import ma
from app.models import Product
from marshmallow import fields # Import fields

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True # Cho phép deserialize thành object Product khi load
        # include_fk = True # Nếu có foreign key và muốn include

    # Thêm validation nếu cần
    name = fields.Str(required=True)
    price = fields.Float(required=True, validate=lambda p: p > 0)
    quantity_in_stock = fields.Int(required=True, validate=lambda q: q >= 0)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)