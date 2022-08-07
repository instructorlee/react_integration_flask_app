from app import app
from app.models.base_models import BaseModel
from app.models.joke_model import JokeModel
from app.models.user_model import UserModel
from app.models.connector import MySQLConnection  

class TopicModel(BaseModel):

    table="topics"
    json_fields = ['id', 'title', 'players', 'setting', 'plot', 'conflict', 'theme', 'narrative_arc', 'jokes', 'users_id']

    basic_select = """
        topics.id AS id,
        title,
        users_id,
        players,
        setting,
        plot,
        conflict,
        theme,
        narrative_arc,

        users.id AS users_id,
        users.email AS users_email
    """

    basic_joins = """

        LEFT JOIN users ON users.id = topics.users_id
    """

    def __init__(self, data):

        self.id = data['id']
        self.title = data['title']
        self.players = data['players']
        self.setting = data['setting']
        self.plot = data['plot']
        self.conflict = data['conflict']
        self.theme = data['theme']
        self.narrative_arc = data['narrative_arc']

        self.user = UserModel({
            'id': data['users_id'],
            'email': data['users_email']
        })

        self._jokes = None

    @property # lazy loading - only loads the jokes data if needed;
    def jokes(self):
        
        if self._jokes is  None:
            self._jokes = JokeModel.filter_all_by({'topics_id': self.id}, jsonify=True)
        
        return self._jokes

    @classmethod
    def add(cls, user, new_topic):

        query = """
            INSERT INTO topics
                (   
                    title,
                    players,
                    setting,
                    plot,
                    conflict,
                    theme,
                    narrative_arc,
                    users_id
                )
            VALUES
                (
                    %(title)s,
                    %(players)s,
                    %(setting)s,
                    %(plot)s,
                    %(conflict)s,
                    %(theme)s,
                    %(narrative_arc)s,
                    {users_id}
                )
        """.format(users_id=user.id)
        
        new_topic_id = MySQLConnection(cls.db).query_db(query, {
            'title': new_topic['title'],
            'players': '' if 'players' not in new_topic else new_topic['players'],
            'setting': '' if 'setting' not in new_topic else new_topic['setting'],
            'plot':  '' if 'plot' not in new_topic else new_topic['plot'],
            'conflict': '' if 'conflict' not in new_topic else new_topic['conflict'],
            'theme': '' if 'theme' not in new_topic else new_topic['theme'],
            'narrative_arc': '' if 'narrative_arc' not in new_topic else new_topic['narrative_arc']
        })
        
        return None if not new_topic_id else cls.get_by_id(new_topic_id)

    @classmethod
    def update(cls, topic, update_data):

        query = """
            UPDATE topics 
            SET 
                title = %(title)s,
                players = %(players)s, 
                setting = %(setting)s, 
                plot = %(plot)s, 
                conflict = %(conflict)s, 
                theme = %(theme)s, 
                narrative_arc = %(narrative_arc)s,
                updated_at = NOW()
            WHERE 
                id = {topic_id}
        """.format(topic_id=topic.id)

        topic_id = MySQLConnection(cls.db).query_db(query, {
            'title': topic.title,
            'players': topic.players if 'players' not in update_data else update_data['players'],
            'setting': topic.setting if 'setting' not in update_data else update_data['setting'],
            'plot':  topic.plot if 'plot' not in update_data else update_data['plot'],
            'conflict': topic.conflict if 'conflict' not in update_data else update_data['conflict'],
            'theme': topic.theme if 'theme' not in update_data else update_data['theme'],
            'narrative_arc': topic.narrative_arc if 'narrative_arc' not in update_data else update_data['narrative_arc']
        })

        return cls.get_by_id(topic.id) if topic_id else None

    @classmethod
    def is_valid(cls, topic):

        return 'title' in topic and topic['title'] != ''

        """
        return ('players' in topic and topic['players']!= '') or \
            ('setting' in topic and topic['setting'] != '') or \
            ('plot' in topic and topic['plot'] != '') or \
            ('conflict' in topic and topic['conflict'] != '') or \
            ('theme' in topic and topic['theme'] != '') or \
            ('narrative_arc' in topic and topic['narrative_arc'] != '')
            """