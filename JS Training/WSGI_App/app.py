import os

from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.wrappers import Request, Response

from jinja2 import Environment, FileSystemLoader
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
import psycopg2



class MovieApp(object):
    """Implements a WSGI application for managing your favorite movies."""
    def __init__(self):
        """Initializes the Jinja templating engine to render from the 'templates' folder."""
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                 autoescape=True)
        self.url_map = Map([
            Rule('/', endpoint='index'),
            Rule('/movies', endpoint='movies'),
            Rule('/add_movie',endpoint='add_movie'),
        ]) 



    def dispatch_request(self, request):
        """Dispatches the request."""
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException as e:
            return e


    def wsgi_app(self, environ, start_response):
        """WSGI application that processes requests and returns responses."""
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """The WSGI server calls this method as the WSGI application."""
        return self.wsgi_app(environ, start_response)

    def render_template(self, template_name, **context):
        """Renders the specified template file using the Jinja templating engine."""
        template = self.jinja_env.get_template(template_name)
        return Response(template.render(context.get('render_context')), mimetype='text/html')

    def index(self, request):
        return self.render_template('base.html')

    def movies(self, request):
        conn = psycopg2.connect(database='wsgi', user='postgres', password='123456', host='localhost', port='5432')
        cur = conn.cursor()
        cur.execute("SELECT * from movie")
        result = cur.fetchall()
        print(result)
        conn.commit()
        return self.render_template('movies.html', render_context={'name':result})

    def add_movie(self, request):
        if request.method=='POST':
            name=request.form['name']
            price=request.form['price']
            conn = psycopg2.connect(database='wsgi', user='postgres', password='123456', host='localhost', port='5432')
            cur = conn.cursor()
            cur.execute("INSERT INTO movie values(%s,%s)",(name,price))
            conn.commit()
        return self.render_template('add_movie.html', render_context={})




def create_app():
    """Application factory function that returns an instance of MovieApp."""
    app = MovieApp()
    return app

if __name__ == '__main__':
    # Run the Werkzeug development server to serve the WSGI application (MovieApp)
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
