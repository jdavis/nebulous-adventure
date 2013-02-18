from base import views as base_views


COMMANDS = {'look':'/look/',
			'move':'/move/', 
			'new':'/new/',
			'resume':'/resume/'}

def apply_urls(app):
    app.add_url_rule('/', view_func=base_views.HomeView.as_view('home'))
    app.add_url_rule('/look/', view_func=base_views.Look.as_view('look'))
    app.add_url_rule('/move/', view_func=base_views.Move.as_view('move'))

    app.add_url_rule('/new/', view_func=base_views.New.as_view('new'))
    app.add_url_rule('/resume/', view_func=base_views.Resume.as_view('resume'))

