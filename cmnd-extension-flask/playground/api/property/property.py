from flask import Flask, request, jsonify, abort, Blueprint
from pydantic import ValidationError
from utils.validators.validators import PropertyCreateRequest
from services.properties.properties import PropertyService
import json

# Create Flask app instance
app = Blueprint('property', __name__, url_prefix='/properties')
# The Blueprint object allows you to modularize your application into smaller pieces and then register them with a Flask application.
# In this case, we're telling Flask that the blueprint's url_prefix is /properties, so all of the routes defined within the blueprint will be prefixed with that.

@app.route("/", methods=['POST'])
def create_property():
    data = request.json
    if not data:
        abort(400, description="Invalid request: JSON data is required")

    try:
        # Validate request body against Pydantic model
        property_data = PropertyCreateRequest(**data).dict()
    except ValidationError as e:
        return jsonify({ 'errors': json.loads(e.json()) }), 400

    try:
        # Create the property using PropertyService
        created_property = PropertyService.create(property_data)
        return jsonify(created_property), 201
    except Exception as e:
        print(e)
        abort(500, description=str(e))

@app.route("/", methods=['GET'])
def get_all_properties():
    try:
        properties = PropertyService.get_all()  # Assuming you have a method to fetch all properties
        return jsonify(properties), 200
    except Exception as e:
        abort(500, description=str(e))
