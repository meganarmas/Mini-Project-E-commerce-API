from flask import request, jsonify
from marshmallow import ValidationError
from app import db, Order, order_schema, orders_schema

@app.route('/orders', methods=['POST'])
def add_order():
    customer_id = request.json['customer_id']
    date = request.json['date']
    total_price = request.json['total_price']
    product = request.json['product']
    status = request.json['status']
    new_order = Order(customer_id=customer_id, date=date, total_price=total_price, product=product, status=status)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify({"message": "New order added successfully"}), 201


@app.route('/orders/<int:id>', methods=['GET'])
def get_orders():
    try:
        all_orders = Order.query(all)
        return jsonify(orders_schema.dump(all_orders))
    except ValidationError as e:
            print(f"Error: {e}")

@app.route('/orders/<int:id>', methods=['GET'])
def get_one_order(id):
    try:
        one_order = Order.query.get(id)
        return order_schema.jsonify(one_order)
    except ValidationError as e:
                print(f"Error: {e}")

@app.route('/orders/<int:id>', methods=['DELETE'])
def cancel_order(id):
    order_delete = Order.query.get_or_404(id)
    if order_delete.status in ['Shipped', 'Delivered']:
        return (400, {"message": "Order cannot be deleted/cancelled as it has already shipped or been deleted."})
    
    order_delete.status = 'Cancelled'
    db.session.delete(order_delete)
    db.session.commit()
    return order_schema.jsonify({"message": "Order was cancelled successfully."}), 200  


@app.route('/orders/<int:id>', methods=['PUT'])
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
def track_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order)