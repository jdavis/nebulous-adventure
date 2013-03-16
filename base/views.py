import json
import logging

from flask import request

from flask.views import MethodView
from flask.templating import render_template

from base import models

game = models.Game()

action_map = {
    'eat': game.eat,
    'examine': game.examine,
    'look': game.look,
    'move': game.move,
    'talk': game.talk,
}


class HomeView(MethodView):
    def get(self):
        return render_template('base.html')


class GameController(MethodView):
    def post(self):
        json_request = json.loads(request.data)
        raw_command = json_request.get('command', '')

        # Split up the command and assign to appropriate variables
        parts = raw_command.split()

        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        action = action_map.get(command, None)

        if action is None:
            logging.info('Invalid command requested {0}'.format(command))
            result = 'That is an invalid command.'
        else:
            logging.info('Calling {0} with args: {0}'.format(command, args))
            try:
                result = action(*args)
            except TypeError:
                logging.info('Not enough arguments given for command {0}'.format(command))
                result = 'Not enough arguments given.'

        return json.dumps({'console': result})
