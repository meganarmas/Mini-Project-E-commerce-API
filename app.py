from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_cors import cross_origin
from marshmallow import fields, Schema, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Calliepeg12!@localhost/e_commerce_api'
db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app)


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
    phone = db.Column(db.String(15))

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

#order
class OrderSchema(ma.Schema):
    status = fields.String(required=True)
    total_price = fields.Float(required=True)

class Meta:
        fields = ("date", "quantity" "total_price", "status")

order_product = db.Table('order_product', 
        db.Column('orders_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
        db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)

)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

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
    customer = db.relationship('Customer', backref='customer_account', uselist=False)

customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)

#products
class ProductsSchema(ma.Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    price = fields.Integer(required=True)

    class Meta:
        fields = ("id", "name", "price", "customer_id")

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    # price = db.relationship('Order', secondary=order_product, backref=db.backref('products'))

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)


#customers
@app.route('/customers', methods=['POST'])
@cross_origin()
def add_customer():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    new_member = Customer(name=name, email=email, phone=phone)
    db.session.add(new_member)
    db.session.commit()
    return customer_schema.jsonify({"message": "New customer added successfully"}), 201

@app.route('/customers/<int:id>', methods=['GET'])
@cross_origin()
def get_customer(id):
    try:
        all_customers = Customer.query.get_or_404(id)
        return customer_schema.jsonify(all_customers)
    except ValidationError as e:
        print(f"Error: {e}")

@app.route('/customer_accounts/<int:id>', methods=['GET'])
@cross_origin()
def get_one_customer(id):
    try:
        one_customer = Customer.query.get(id)
        return customer_schema.jsonify(one_customer)
    except ValidationError as e:
                print(f"Error: {e}")

@app.route('/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_customer(id):
    remove_customer = Customer.query.get_or_404(id)
    db.session.delete(remove_customer)
    db.session.commit()
    return customer_schema.jsonify({"message": "Customer's information deleted successfully."}), 200  


@app.route('/customers/<int:id>', methods=['PUT'])
@cross_origin()
def update_customer():
    update_customer = Customer.query.get_or_404(id)
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    update_customer.name = name
    update_customer.email = email
    update_customer.phone = phone
    db.session.commit()
    return customer_schema.jsonify(update_customer)

@app.route('/orders', methods=['POST'])
@cross_origin()
def add_order():
    customer_id = request.json['customer_id']
    status = request.json['status']
    total_price = request.json['total_price']
    new_order = Order(customer_id=customer_id, total_price=total_price, status=status)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify({"message": "New order added successfully"}), 201

#orders
@app.route('/orders/<int:id>', methods=['GET'])
@cross_origin()
def get_orders(id):
    try:
        all_orders = Order.query.get_or_404(id)
        return order_schema.jsonify(all_orders)
    except ValidationError as e:
            print(f"Error: {e}")

@app.route('/orders/<int:id>', methods=['GET'])
@cross_origin()
def get_one_order(id):
    try:
        one_order = Order.query.get_or_404(id)
        return order_schema.jsonify(one_order)
    except ValidationError as e:
                print(f"Error: {e}")

@app.route('/orders/<int:id>', methods=['DELETE'])
@cross_origin()
def cancel_order(id):
    order_delete = Order.query.get_or_404(id)
    if order_delete.status in ['Shipped', 'Delivered']:
        return (400, {"message": "Order cannot be deleted/cancelled as it has already shipped or been deleted."})
    
    order_delete.status = 'Cancelled'
    db.session.delete(order_delete)
    db.session.commit()
    return order_schema.jsonify({"message": "Order was cancelled successfully."}), 200  


@app.route('/orders/<int:id>', methods=['PUT'])
@cross_origin()
def update_order():
    update_order = Order.query.get_or_404(id)
    customer_id = request.json['customer_id']
    date = request.json['date']
    total_price = request.json['total_price']
    status = request.json['status']
    update_order.customer_id = customer_id
    update_order.date = date
    update_order.total_price = total_price
    update_order.status = status
    db.session.commit()
    return order_schema.jsonify(update_order)

@app.route('/orders/<int:id>', methods=['GET'])
@cross_origin()
def track_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order)

# customer account
@app.route('/customer_accounts', methods=['POST'])
@cross_origin()
def add_customer_account():
    username = request.json['username']
    password = request.json['password']
    customer_id = request.json['customer_id']
    new_account = CustomerAccount(username=username, password=password, customer_id=customer_id)
    db.session.add(new_account)
    db.session.commit()
    return customer_account_schema.jsonify({"message": "New customer account added successfully"}), 201


@app.route('/customer_accounts/<int:id>', methods=['GET'])
@cross_origin()
def get_all_customer_account():
    try:
        all_customers_accounts = CustomerAccount.query(all)
        return jsonify(customer_accounts_schema.dump(all_customers_accounts))
    except ValidationError as e:
        print(f"Error: {e}")

@app.route('/customer_accounts/<int:id>', methods=['GET'])
@cross_origin()
def get_customer_account(id):
    try:
        one_account = CustomerAccount.query.get(id)
        return customer_account_schema.jsonify(one_account)
    except ValidationError as e:
                print(f"Error: {e}")

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return customer_account_schema.jsonify({"message": "Customer Account was deleted successfully."}), 200  


@app.route('/customer_accounts/<int:id>', methods=['PUT'])
@cross_origin()
def update_customer_account():
    update_account = CustomerAccount.query.get_or_404(id)
    username = request.json['username']
    password = request.json['password']
    customer_id = request.json['customer_id']
    update_account.username = username
    update_account.password = password
    update_account.customer_id = customer_id
    db.session.commit()
    return customer_account_schema.jsonify(update_account)

#products
@app.route('/products', methods=['POST'])
@cross_origin()
def add_product():
    name = request.json['name']
    price = request.json['price']
    print(request.json)
    new_product = Products(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify({"message": "New product added successfully"}), 201


@app.route('/products/<int:id>', methods=['GET'])
@cross_origin()
def get_products():
    try:
        all_products = Products.query(all)
        return jsonify(products_schema.dump(all_products))
    except ValidationError as e:
            print(f"Error: {e}")

@app.route('/products/<int:id>', methods=['GET'])
@cross_origin()
def get_one_product(id):
    try:
        one_product = Products.query.get_or_404(id)
        return product_schema.jsonify(one_product)
    except ValidationError as e:
                print(f"Error: {e}")

@app.route('/products/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_product(id):
    delete_product = Products.query.get_or_404(id)
    db.session.delete(delete_product)
    db.session.commit()
    return product_schema.jsonify({"message": "Customer Account was deleted successfully."}), 200  


@app.route('/products/<int:id>', methods=['PUT'])
@cross_origin()
def update_product_info(id):
    update_product = Products.query.get_or_404(id)
    name = request.json['name']
    price = request.json['price']
    update_product.name = name
    update_product.price = price
    db.session.commit()
    return product_schema.jsonify(update_product)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
