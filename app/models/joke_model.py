from app import app
from app.models.base_models import BaseModel
from flask_app.app.models.connector import MySQLConnection 

class JokeModel(BaseModel):

    table="jokes"
    json_fields=['id', 'text', 'topics_id']

    def __init__(self, data):

        self.id = data['id']
        self.text = data['text']
        self.topics_id = data['topics_id']

    @classmethod
    def add(cls, user, new_item):

        query = """
            INSERT INTO jokes
                (   
                    text,
                    topics_id,
                    users_id
                )
            VALUES
                (
                    %(text)s,
                    %(topics_id)s,
                    {users_id}
                )
        """.format(users_id=user.id)
        
        new_item_id = MySQLConnection(cls.db).query_db(query, new_item)
        
        return None if not new_item_id else cls.get_by_id(new_item_id)

    @classmethod
    def update(cls, original, update_data):

        query = """
            UPDATE {table} 
            SET 
                text = %(text)s,
                updated_at = NOW()
            WHERE 
                id = {id}
        """.format(table=cls.table, id=original.id)

        topic_id = MySQLConnection(cls.db).query_db(query, {
            'text': original.text if 'text' not in update_data else update_data['text']
        })

        return cls.get_by_id(original.id)

    @classmethod
    def is_valid(cls, data):
        return 'text' in data and data['text'] != ''
