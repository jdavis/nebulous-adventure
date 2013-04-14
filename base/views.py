import json
import logging
import os

from flask import request, session

from flask.views import MethodView
from flask.templating import render_template


from base.models import GameController

# Game to Map to
game = GameController()

action_map = {
    'eat': game.eat,
    'examine': game.examine,
    'look': game.look,
    'move': game.move,
    'talk': game.talk,
    'take': game.take,
    'help': game.help,
}


class HomeView(MethodView):
    def get(self):
        if 'uid' not in session:
            session['uid'] = os.urandom(24)

        return render_template('base.html')


class GameView(MethodView):
    def get(self):
        return json.dumps(action_map.keys())

    def post(self):
        if 'uid' not in session:
            session['uid'] = os.urandom(24)

        uid = session['uid'].encode('hex')

        json_request = json.loads(request.data)
        raw_command = json_request.get('command', '')

        # Split up the command and assign to appropriate variables
        parts = raw_command.split()

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
            try:
                result = action(uid, *args)
            except TypeError, e:
                logging.error('Got error {0}'.format(e))
                logging.info('Not enough arguments given for command {0}'.format(command))
                result = 'Not enough arguments given.'

        return json.dumps({'console': result})
