from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage

@app_views.route('/states', methods=['GET'])
def get_states():
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({})

@app_views.route('/states', methods=['POST'])
def create_state():
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
