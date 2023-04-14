#!/usr/bin/python3
"""Places Routes"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    '/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_cities(city_id):
    """ retrieves all places in a city """
    place = storage.get(City, city_id)
    if place is None:
        abort(404)
    places = []
    for i in storage.all('Place').values():
        if i.city_id == city_id:
            i.append(place.to_dict())
    return jsonify(places)


@ app_views.route('/places/<place_id>', methods=['GET'])
def place(place_id):
    """returns place of id given"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict()), 200


@ app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """create a place and link to city"""
    data = request.get_json(silent=True)
    if data is None:
        return 'Not a JSON', 400
    elif 'name' not in data.keys():
        return 'Missing name', 400
    elif 'user_id' not in data.keys():
        return 'Missing user_id', 400

    print(data)
    if storage.get(User, data['user_id']) is None\
            or storage.get(City, city_id) is None:
        abort(404)

    new_place = Place(**data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@ app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """updates given place"""
    find = storage.get(Place, place_id)
    if find is None:
        return '', 404

    data = request.get_json(silent=True)
    if data is None:
        return 'Not a JSON', 400

    for key, values in data.items():
        if key not in ['id', 'user_id', 'city_id' 'created_at', 'updated_at']:
            setattr(find, key, values)

    storage.save()
    return jsonify(find.to_dict()), 200


@ app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """DELETE place if id is found"""
    place = storage.get(Place, place_id)
    if place is None:
        return '{}', 404

    storage.delete(place)
    storage.save()
    return jsonify({}), 200
