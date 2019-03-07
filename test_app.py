from flask import Flask, render_template, flash, redirect, request, url_for
from config import Config
from forms import LoginForm, SignUpForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from models import User

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

#######################################	



@app.route("/index")
def hello():
	return "Hello World!"

from flask_login import current_user, login_user
@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('hello'))

	form = LoginForm()
	if request.method=='POST' and form.validate_on_submit():
		if form.check():
			return redirect(url_for('hello'))			
	else:
		print(form.errors)
		print('something gone wrong')
	return render_template('login.html', title = 'Login', form = form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	forms = SignUpForm()
	if request.method=='POST' and forms.validate_on_submit():		
		return redirect(url_for('login'))	
	else:		
		print(forms.errors)

	print('и туть')	
	return render_template('signup.html', title = 'SignUp', form = forms)
