from app import db
from datetime import datetime, timezone

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False, default=0)
    sku = db.Column(db.String(50), unique=True, nullable=True, index=True)
    date_added = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Product {self.name}>'