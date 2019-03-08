from flask import (Flask, render_template, flash, redirect, request, url_for,
	jsonify, Response)
from config import Config, db, migrate, app
from auth import login
from auth.forms import LoginForm, SignUpForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, logout_user, current_user, login_user,
	login_required)
from auth.models import User
import json
import os

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

#######################################	
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User}

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('hello'))

	forml = LoginForm()
	if request.method=='POST' and forml.validate_on_submit():
		user = User.query.filter_by(username = forml.username.data).first()
		
		if forml.checkx(user = user):
			
			login_user(user, remember = True)
			return redirect(url_for('hello'))		
	else:
		print(forml.errors)
		print('something gone wrong')
	return render_template('login.html', title = 'Login', form = forml)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	forms = SignUpForm()
	if request.method=='POST' and forms.validate_on_submit():
		if forms.check_user_exists() == False:
			user = User(username = forms.username.data, name = forms.name.data)
			user.set_password(forms.password.data)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('login'))	
	else:		
		print(forms.errors)

	return render_template('signup.html', title = 'SignUp', form = forms)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/index')
def hello():
	return render_template('index.html', title = 'hello', username = current_user.username)

