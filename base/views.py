import json
import logging
import os

from flask import request, session

from flask.views import MethodView
from flask.templating import render_template

from base.game_controller import GameController


class HomeView(MethodView):
    def get(self):
        if 'uid' not in session:
            session['uid'] = os.urandom(24).encode('hex')

        return render_template('base.html')


class GameView(MethodView):
    def post(self):
        uid = session['uid']

        json_request = json.loads(request.data)
        raw_command = json_request.get('command', '')
        temp_key = json_request.get('tempKey', None)

        # Game to Map to
        game = GameController(uid, temp_key=temp_key)

        action_map = {
            'attack': game.attack,
            'die': game.die,
            'eat': game.eat,
            'examine': game.examine,
            'help': game.help,
            'inventory': game.inventory,
            'look': game.look,
            'move': game.move,
            'put': game.put,
            'save': game.save,
            'start': game.start,
            'welcome': game.welcome,
            'take': game.take,
            'talk': game.talk,
            'use': game.use,
        }

        # Split up the command and assign to appropriate variables
        parts = raw_command.lower().split()

        if len(parts) == 0:
            return json.dumps({'console': 'I can\'t hear you, say it louder'})

        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        action = action_map.get(command, None)

        if action is None:
            logging.info('Invalid command requested {0}'.format(command))
            result = 'That is an invalid command.'
        else:
            logging.info('Calling {0} with args: {1}'.format(command, ','.join(args)))
            result = action(*args)

        if type(result) == str or type(result) == unicode:
            payload = {
                'console': result,
            }
        else:
            payload = result

        return json.dumps(payload)
