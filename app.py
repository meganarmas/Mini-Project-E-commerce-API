from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = ['mysql+mysqlconnector://root:{Calliepeg12!}@localhost/e_commerce_api']
db = SQLAlchemy(app)
ma = Marshmallow(app)

#define_all_schemas
#customer

class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

class Meta:
        fields = ("id", "name", "email", "phone")

class Customer (db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320))
    phone = db.Colum(db.String(15))

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

#order

order_product = db.Table('order_product', 
        db.Column('order_id', db.Integer, db.ForeginKey('orders.id'), primary_key=True),
        db.Column('product_id', db.Integer, db.ForeginKey('products.id'), primary_key=True)

)

class OrderSchema(ma.Schema):
    name = fields.String(required=True)
    date = fields.Date(required=True)
    delivery_status = fields.String(required=True)
    total_price = fields.Float(required=True)

class Meta:
        fields = ("id", "date", "total_price", "delivery_status")

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    delivery_status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    product = db.relationship('order', secondary=order_product, backref=db.backref('products'))

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

#customeraccounts

class CustomerAccountSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Integer(required=True)
    customer = fields.Nested('CustomerSchema', only=['name', 'email', 'phone'])

class Meta:
        fields = ("id", "username", "password", "customer_id", "customer")


class CustomerAccount(db.Model):
    __tablename__ = 'customer_accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', backred='customer_account', uselist=False)

customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)

#products
class ProductsSchema(ma.Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)

    class Meta:
        fields = ("id", "name", "price", "customer_id")

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    price = db.relationship('order', secondary=order_product, backref=db.backref('products'))

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)