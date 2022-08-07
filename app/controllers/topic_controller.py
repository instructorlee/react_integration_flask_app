from flask import jsonify, request, session
from app import app

from app.decorators import jwt_required
from app.models.topic_model import TopicModel

@app.route('/topic/add', methods=['POST'])
@jwt_required
def add_topic(user, data):
    
    if TopicModel.is_valid(data):
        new_topic = TopicModel.add(user, data)

        if new_topic is not None:
            return jsonify(new_topic.to_json()), 200
        
    return jsonify({}), 422

@app.route('/topic/update', methods=['POST'])
@jwt_required
def update_topic(user, data):

    topic = TopicModel.filter_one_by({ 
        'users_id': user.id,
        'id': data['id']
    })

    if topic is not None and TopicModel.is_valid(data):
        updated_topic = TopicModel.update(topic, data)
        if updated_topic:
            return jsonify(updated_topic.to_json()), 200
        
    return jsonify({}), 422

@app.route('/topic/delete/<id>')
@jwt_required
def delete_topic(id, user, *args, **kwargs):

    topic = TopicModel.filter_one_by({ 
        'users_id': user.id,
        'id': id
    })

    if topic is not None:
        TopicModel.delete(id)
        return jsonify({'status': 'ok'}), 201

    return jsonify({}), 422

@app.route('/topic/<id>')
@jwt_required
def get_topic(id, user, *args, **kwargs):

    item = TopicModel.filter_one_by({ 
        'users_id': user.id,
        'topics.id': id
    })

    if item is not None:
        return jsonify(item.to_json()), 200

    return jsonify({}), 422

@app.route('/topic/my')
@jwt_required
def get_my_topics(user, *args, **kwargs):
    
    return jsonify(TopicModel.filter_all_by({'users_id': user.id}, jsonify=True)), 200
