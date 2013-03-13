from flask.views import MethodView
from flask.templating import render_template
from flask import request
import json

class HomeView(MethodView):
    def get(self):
        return render_template('base.html')

class GameController(MethodView):
    def post(self):
        json_request = json.loads(request.data)
        command = json_request.get('command','')
        return json.dumps({'console': command})
