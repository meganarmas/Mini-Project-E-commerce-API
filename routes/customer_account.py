from flask import request, jsonify
from marshmallow import ValidationError
from app import db, CustomerAccount, customer_account_schema, customer_accounts_schema


@app.route('/customer_accounts', methods=['POST'])
def add_customer_account():
    username = request.json['username']
    password = request.json['password']
    customer_id = request.json['customer_id']
    new_account = CustomerAccount(username=username, password=password, customer_id=customer_id)
    db.session.add(new_account)
    db.session.commit()
    return customer_account_schema.jsonify({"message": "New customer account added successfully"}), 201


@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_customer_account():
    try:
        all_customers_accounts = CustomerAccount.query(all)
        return jsonify(customer_accounts_schema.dump(all_customers_accounts))
    except ValidationError as e:
        print(f"Error: {e}")

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_customer_account(id):
    try:
        one_account = CustomerAccount.query.get(id)
        return customer_account_schema.jsonify(one_account)
    except ValidationError as e:
                print(f"Error: {e}")

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return customer_account_schema.jsonify({"message": "Customer Account was deleted successfully."}), 200  


@app.route('/customer_accounts/<int:id>', methods=['PUT'])
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