from flask import jsonify, request, session
from app import app

from app.decorators import jwt_required
from app.models.joke_model import JokeModel
from app.models.topic_model import TopicModel

@app.route('/joke/add', methods=['POST'])
@jwt_required
def add_joke(user, data):

    if JokeModel.is_valid(data) and'topic_id' in data and data['topic_id'] != '':
            topic = TopicModel.get_by_id(data['topic_id'])

            if topic is not None and topic.user.id == user.id:
                data['topics_id'] = data['topic_id'] # needed to make front end compatiable with both backends.
                new_item = JokeModel.add(user, data)

                if new_item is not None:
                    return jsonify(new_item.to_json()), 200
        
    return jsonify({}), 422

@app.route('/joke/update', methods=['POST'])
@jwt_required
def update_joke(user, data):

    item = JokeModel.filter_one_by({ 
        'users_id': user.id,
        'id': data['id']
    })

    if item is not None and JokeModel.is_valid(data):
        updated_item = JokeModel.update(item, data)
        if updated_item:
            return jsonify(updated_item.to_json()), 200
        
    return jsonify({}), 422

@app.route('/joke/delete/<id>', methods=['DELETE'])
@jwt_required
def delete_joke(id, user, *args, **kwargs):

    item = JokeModel.filter_one_by({ 
        'users_id': user.id,
        'id': id
    })

    if item is not None:
        JokeModel.delete(id)
        return jsonify({'status': 'ok'}), 201

    return jsonify({}), 422
