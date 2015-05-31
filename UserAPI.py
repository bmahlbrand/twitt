from flask.views import MethodView

class UserAPI(MethodView):

	def get(self, user_id):
		if user_id is None:
			# return a list of users
			pass
		else:
			# expose a single user
			pass

	def post(self):
		# create a new user
		pass

	def delete(self, user_id):
		# delete a single user
		pass

	def put(self, user_id):
		# update a single user
		pass

user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/users/', view_func=user_view, methods=['POST',])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])