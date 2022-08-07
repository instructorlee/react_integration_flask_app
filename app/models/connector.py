
import pymysql.cursors
import os

# from pyparsing import null_debug_action

class MySQLConnection:

	def __init__(self, db):

		# change the user and password as needed in flask_app/config/.env
		connection = pymysql.connect(host='localhost',
									user='root',
									password='rootroot',
                    				db=db,
									charset='utf8mb4',
									cursorclass=pymysql.cursors.DictCursor,
									autocommit=True)
		# establish the connection to the database
		self.connection = connection

	def get_result(self, query = None, data = None, _cls = None, jsonify = False):
		results = self.query_db(query=query, data=data)

		if not results or len(results) == 0:
			return None

		elif _cls is None: # no CLS given, return raw results
			return results[0]

		else:
			if jsonify:
				return _cls(results[0]).to_json()
			else:
				return _cls(results[0])

	def get_results(self, query = None, data = None, _cls = None, jsonify = False):

		results = self.query_db(query=query, data=data)

		if _cls is None: # no CLS given, return raw results
			return results

		else:
			if jsonify:
				return [_cls(result).to_json() for result in results]
			else:
				return [_cls(result) for result in results]

	def query_db(self, query, data=None):
		with self.connection.cursor() as cursor:
			try:
				query = cursor.mogrify(query, data)
				cursor.execute(query, data)
				if query.lower().find("insert") >= 0:
					self.connection.commit()
					return cursor.lastrowid

				elif query.lower().find("select") >= 0:
					result = cursor.fetchall()
					return result

				elif query.lower().find("update") >= 0:
					return True

				else: # delete
					self.connection.commit()
					
			except Exception as e:
				# if the query fails the method will return FALSE
				print(query)
				print('Something went wrongx', e)
				return False

			finally:
				# close the connection
				self.connection.close()
