from flask import Flask, request, jsonify
from app import db, Customer, customer_schema, customers_schema

@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    new_member = Customer(name=name, email=email, phone=phone)
    db.session.add(new_member)
    db.session.commit()
    return customer_schema.jsonify({"message": "New customer added successfully"}), 201


@app.route('/customers/<int:id>', methods=['GET'])
def get_customer():
    all_customers = Customer.query(all)
    return jsonify(customers_schema.dump(all_customers))

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return customer_schema.jsonify({"message": "Customer's information deleted successfully."}), 200  


@app.route('/customers/<int:id>', methods=['PUT'])
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