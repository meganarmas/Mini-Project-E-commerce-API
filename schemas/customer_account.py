from flask import Flask, request, jsonify
from app import db, CustomerAccount, customer_account_schema, customer_accounts_schema

@app.route('/ccstomer_accounts', methods=['POST'])
def add_customer_account():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    new_member = CustomerAccount(name=name, email=email, phone=phone)
    db.session.add(new_member)
    db.session.commit()
    return customer_schema.jsonify({"message": "New customer account added successfully"}), 201


@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_customer_account():
    all_customers_accounts = CustomerAccount.query(all)
    return jsonify(customers_schema.dump(all_customers_accounts))

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return customer_account_schema.jsonify({"message": "Customer Account was deleted successfully."}), 200  


@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account():
    member = CustomerAccount.query.get_or_404(id)
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    member.name = name
    member.email = email
    member.phone = phone
    db.session.commit()
    return customer_account_schema.jsonify(member)