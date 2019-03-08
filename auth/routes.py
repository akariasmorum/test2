from flask import (Flask, render_template, flash, redirect, request, url_for,
	jsonify, Response)
from config import Config
from auth.forms import LoginForm, SignUpForm, InsertForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, logout_user, current_user, login_user,
	login_required)
from auth.models import User
import json
from auth import db, migrate, login, app


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
		print(12)
		if forml.checkx(user = user):
			print(13)
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




@app.route('/form', methods = ['POST', 'GET'])
@login_required
def json_form():
	form = InsertForm()
	if request.method == 'POST' and form.validate_on_submit():
		try:
			json_text = json.loads(form.text.data)
			
		except Exception as ex:
			return str(ex)	

		ct = dict(form.command_type.choices).get(form.command_type.data)
		return dispatcher(ct, json_text)

	else:		
		print(form.errors)

	return render_template('form.html', title = 'Form', form = form)		

def dispatcher(com_type, json_text):
	disp_dict = {
		"POST": insert_user,
		"PUT": update_user,
		"DELETE": delete_user, 
	}

	return disp_dict[com_type](json_text)

def all_user():
	users = User.query.all()
	users_js = []
	for user in users:
		users_js.append(
			{
				"id": user.id,
				"username": user.username,
				"name": user.name
			})

	return jsonify(users_js)	


@app.route('/api/user/<int:id>')
@login_required
def get_user(id):
	user = User.query.filter_by(id = id).first()
	if user!=None:
		response = {
			"username": user.username,
			"name": user.name,	
		}
		return jsonify(response)

	else:		
		return Response("Такого пользователя нет", status=400)


@app.route('/api/update', methods = ['POST'])
@login_required
def update_user(json_text):
	for user_js in json_text:		
		user = User.query.filter_by(id = user_js['id']).first()
		if user!=None:
			user.name = user_js['name']
			try:
				db.session.commit()				
			except Exception as ex:
				error =  "user: {0} произошла ошибка обновления: {1}".format(
					user_js, str(ex))
				return Response(error, status = 500)
		else:
			error =  "user_id: {0}  - Такого пользователя нет".format(user_js['id'])
			return Response(error, status = 400)

	return all_user()		

@app.route('/api/delete', methods = ['POST'])
@login_required
def delete_user(json_text):
	for user_js in json_text:

		user = User.query.filter_by(id = user_js['id']).first()

		if user!=None:					
			try:
				db.session.delete(user)	
				db.session.commit()			
			except Exception as ex:
				error = "user: {0} произошла ошибка удаления: {1} ".format(
					user_js, ex)
				return Response(error, status = 500)	
		else:
			error =  "user_id: {0}  - Такого пользователя нет".format(user_js['id'])
			return Response(error, status = 400)	

	return all_user()					



@app.route('/api/delete', methods = ['POST'])
@login_required
def insert_user(json_text):
	for user_js in json_text:
		try:
			user = User(username = user_js['username'], name = user_js['name'])
			user.set_password(user_js['password'])			
			db.session.commit()
			
		except Exception as ex:
			return "user: {0} произошла ошибка вставки: {1}".format(
					user_js, str(ex))

	return all_user()	



	
