from flask.views import MethodView
from flask.templating import render_template

class HomeView(MethodView):
    def get(self):
        return render_template('base.html')

