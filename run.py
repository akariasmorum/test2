from config import app, db
from auth.models import User
from werkzeug.contrib.fixers import ProxyFix
import api

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User}

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
	app.run()