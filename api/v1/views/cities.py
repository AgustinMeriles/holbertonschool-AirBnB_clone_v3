#!/usr/bin/python3
"""new view for City objects that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models.state import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """returns citys for a state given"""


    states = storage.get(State, state_id)
    if states is None:
        abort(404)

    list_of_cities = states.cities
    citys_dict = []

    for city in list_of_cities:
        citys_dict.append(city.to_dict())

    return jsonify(citys_dict)


@app_views.route('/cities/<city_id>', methods=['GET'])
def cities(city_id):
    """returns city of id given"""


    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """create a city and links to state"""


    data = request.get_json(silent=True)
    if data is None:
        return 'Not a JSON', 400
    elif 'name' not in data.keys():
        return 'Missing name', 400
    elif storage.get(State, state_id) is None:
        abort(404)

    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """updates given city"""


    city = storage.get(City, city_id)

    if city is None:
        return '', 404

    data = request.get_json(silent=True)
    if data is None:
        return 'Not a JSON', 400

    for key, values in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, values)

    storage.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """DELETE city if id is found"""


    city = storage.get(City, city_id)
    if city is None:
        return '{}', 404

    storage.delete(city)
    storage.save()
    return jsonify({}), 200
