from flask import Flask, request, jsonify
from app import db, Order, order_schema, orders_schema

@app.route('/orders', methods=['POST'])
def add_order():
    customer_id = request.json['customer_id']
    date = request.json['date']
    total_price = request.json['total_price']
    product = request.json['product']
    new_order = Order(customer_id=customer_id, date=date, total_price=total_price, product=product)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify({"message": "New order added successfully"}), 201


@app.route('/orders/<int:id>', methods=['GET'])
def get_orders():
    all_orders = Order.query(all)
    return jsonify(orders_schema.dump(all_orders))

@app.route('/orders/<int:id>', methods=['GET'])
def get_one_order(id):
    one_order = Order.query.get(id)
    return order_schema.jsonify(one_order)

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order_to_delete = Order.query.get_or_404(id)
    db.session.delete(order_to_delete)
    db.session.commit()
    return order_schema.jsonify({"message": "Customer Account was deleted successfully."}), 200  


@app.route('/orders/<int:id>', methods=['PUT'])
def update_order():
    update_order = Order.query.get_or_404(id)
    customer_id = request.json['customer_id']
    date = request.json['date']
    total_price = request.json['total_price']
    delivery_status = request.json['delivery_status']
    update_order.customer_id = customer_id
    update_order.date = date
    update_order.total_price = total_price
    update_order.delivery_status = delivery_status
    db.session.commit()
    return order_schema.jsonify(update_order)