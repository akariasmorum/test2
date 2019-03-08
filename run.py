from auth import app, db
from auth.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}