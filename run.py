from config import app, db
from auth.models import User
import api

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User}

if __name__ == '__main__':
	app.run()