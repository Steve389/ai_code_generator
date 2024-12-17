add_item = FlaskBlueprint("", __name__).route('/add\_item/\<int:order\_id\>').method('POST')
def add\_item(order\_id):
	order\_item = request.json
	# Your code to add new order item here
	return jsonify({'message': 'Item added successfully'})