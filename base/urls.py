from base import views as base_views

def apply_urls(app):
    app.add_url_rule('/', view_func=base_views.HomeView.as_view('home'))
