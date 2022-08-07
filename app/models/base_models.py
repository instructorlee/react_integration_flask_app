
from app.models.connector import MySQLConnection

class BaseModel:

    db="joke_generator_flask"
    table = ""

    json_fields = [] # which fields to allow when .to_json()

    basic_select = "*"
    basic_joins = ""

    def __init__(self, data):
        
        for key in data:
            setattr(self, key, data[key])
    
    def to_json(self, add_fields=[], fields=[]): # fields will replace default fields

        fields = fields if len(fields) > 0 else self.json_fields

        ret = {}
        for field in fields + add_fields:
            if hasattr(self, field): # check if exists in the object being serialized
                ret[field] = getattr(self, field)

        return ret

    @classmethod
    def build_where_filters(cls, criteria):

        filter = ""
        
        for index, key in enumerate(criteria):

            if ( index > 0 ):
                filter += ' and '

            filter += " {key}='{value}'".format( key = key, value = criteria[key])
        
        return filter

    @classmethod
    def get_by_id(cls, id, jsonify = False):

        query = """
            SELECT 
                {select} 
            FROM {table} 
            {joins}
            WHERE {table}.id={id}
        """.format(select = cls.basic_select, table=cls.table, joins=cls.basic_joins, id=id)

        return MySQLConnection(cls.db).get_result(query=query, _cls=cls, jsonify=jsonify)

    @classmethod
    def filter_all_by(cls, criteria = {}, jsonify = False):
        query = """
            SELECT {select} FROM {table} {joins} WHERE {filters}
        """.format( select = cls.basic_select, table=cls.table, joins=cls.basic_joins, filters = cls.build_where_filters(criteria=criteria) )

        return MySQLConnection(cls.db).get_results(query = query, _cls = cls, jsonify=jsonify)

    @classmethod
    def filter_one_by(cls, criteria = {}, jsonify = False):
        
        query = """
            SELECT {select} FROM {table} {joins} WHERE {filters}
        """.format( select = cls.basic_select, table=cls.table, joins=cls.basic_joins, filters = cls.build_where_filters(criteria=criteria) )
        
        return MySQLConnection(cls.db).get_result(query = query, _cls = cls, jsonify=jsonify)

    @classmethod
    def get_all(cls, jsonify = False):

        query = """
            SELECT {select} FROM {table} {joins}
        """.format(select = cls.basic_select, table=cls.table, joins=cls.basic_joins)

        return MySQLConnection(cls.db).get_results(query = query, _cls = cls, jsonify=jsonify)

    @classmethod
    def delete(cls, id):

        query = """
            DELETE FROM {table}  WHERE id={id}
        """.format(table=cls.table, id=id)

        return MySQLConnection(cls.db).query_db(query = query)

