from flask import Flask, request, jsonify
from app import db, Products, product_schema, products_schema

@app.route('/products', methods=['POST'])
def add_order():
    name = request.json['name']
    price = request.json['price']
    new_product = Products(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify({"message": "New product added successfully"}), 201


@app.route('/products/<int:id>', methods=['GET'])
def get_orders():
    all_products = Products.query(all)
    return jsonify(products_schema.dump(all_products))

@app.route('/orders/<int:id>', methods=['GET'])
def get_one_order(id):
    one_product = Products.query.get(id)
    return product_schema.jsonify(one_product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    delete_product = Products.query.get_or_404(id)
    db.session.delete(delete_product)
    db.session.commit()
    return product_schema.jsonify({"message": "Customer Account was deleted successfully."}), 200  


@app.route('/products/<int:id>', methods=['PUT'])
def update_product_info():
    update_product = Products.query.get_or_404(id)
    name = request.json['name']
    price = request.json['price']
    update_product.name = name
    update_product.price = price
    db.session.commit()
    return product_schema.jsonify(update_product)