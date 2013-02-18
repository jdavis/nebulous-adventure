from flask.views import MethodView
from flask.templating import render_template
from flask import request, make_response
import urls
import json
import logging
from base import utils as Game

class HomeView(MethodView):
    def get(self):

        return render_template('base.html')

class Look(MethodView):
	def get(self):
		args = request.args.get('args', '').split(' ')
		uid = request.cookies.get('nebuid')
		
		dir_description = Game.look(uid,str(args[0]))

		return json.dumps({'console':dir_description})

class Move(MethodView):
	def get(self):
		args = request.args.get('args', '').split(' ')
		uid = request.cookies.get('nebuid')
		
		description = Game.look(uid,args[0])

		return json.dumps({'console':description})

class New(MethodView):
	def get(self):
		response = make_response(json.dumps({'console':'New game created...', 'new_commands':urls.COMMANDS}))
		# response.set_cookie('nebuid', actions.create_new_world())
		response.set_cookie('nebuid', 'ahZkZXZ-bmVidWxvdXMtYWR2ZW50dXJlcgsLEgVXb3JsZBg9DA')
		return response

class Resume(MethodView):
	def get(self):
		pass
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
