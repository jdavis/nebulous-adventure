from flask.views import MethodView
from flask.templating import render_template
from flask import request, make_response
import urls
import json
import logging
from base.utils import Game

class HomeView(MethodView):
    def get(self):

        return render_template('base.html')

class GameController(MethodView):
	def get(self):
		user_input = request.args.get('command', '').split(' ')
		command = user_input.pop(0)

		if command == 'new':
			# this takes the first argument of this command and sets it as your
			# nebuid cookie
			#
			response = make_response(json.dumps({'console':'New game created...'}))
			# response.set_cookie('nebuid', actions.create_new_world())
			response.set_cookie('nebuid', user_input[0])
			return response
		else:
			uid = request.cookies.get('nebuid')

			to_execute = Game().command_dict.get(command,None)
			game_response = 'What?'

			if to_execute is not None:
				game_response = to_execute(Game, uid, user_input)

			return json.dumps({'console':game_response})


# class New(MethodView):
# 	def get(self):
# 		response = make_response(json.dumps({'console':'New game created...', 'new_commands':urls.COMMANDS}))
# 		# response.set_cookie('nebuid', actions.create_new_world())
# 		response.set_cookie('nebuid', 'ahZkZXZ-bmVidWxvdXMtYWR2ZW50dXJlcgsLEgVXb3JsZBg9DA')
# 		return response

# class Resume(MethodView):
# 	def get(self):
# 		pass
		# args = request.args.get('args', '').split(' ')
		# text_response = ''
		# saved_world = None

		# if args:
		# 	saved_world = actions.get_world_by_key(args[0])
		# 	text_response = 'Successfully loaded game...' if saved_world is not None else 'Save not found...'
		# else:
		# 	text_response = 'Invalid arguments...'

		# response = make_response(json.dumps({'console':text_response, 'new_commands':urls.COMMANDS}))

		# if saved_world is not None:
		# 	response.set_cookie('nebuid', saved_world.key())

		# return response
