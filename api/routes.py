from flask import request, Response, jsonify, render_template
from config import app, db
from api.forms import InsertForm
import json
from auth.models import User
from flask_login import (LoginManager, logout_user, current_user, login_user,
	login_required)
import os
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect(app)




@app.route('/form', methods = ['POST', 'GET'])
@login_required
def json_form():
	form = InsertForm()
	i_js, d_js, u_js = load_json()
	if request.method == 'POST' and form.validate_on_submit():
		try:
			json_text = json.loads(form.text.data)
			
		except Exception as ex:
			return str(ex)	

		ct = dict(form.command_type.choices).get(form.command_type.data)
		return dispatcher(ct, json_text)

	else:

		print(form.errors)

	return render_template('form.html', title = 'Form', form = form,
		insert_json = i_js, 
		delete_json = d_js,
		put_json = u_js)		

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


@app.route('/api/user/<int:id>', methods = ['GET'])
@login_required
@csrf.exempt
def get_user(id):
	if id == 0:
		return all_user()

	user = User.query.filter_by(id = id).first()
	if user!=None:
		response = {
			"username": user.username,
			"name": user.name,	
		}
		return jsonify(response)

	else:		
		return Response("Такого пользователя нет", status=400)


@app.route('/api/user', methods = ['PUT'])
@login_required
@csrf.exempt
def update_user():
	json_text = json.loads(request.json['data'])
	print(json_text)
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


@app.route('/api/user/', methods = ['DELETE'])
@login_required
@csrf.exempt
def delete_user():
	json_text = json.loads(request.json['data'])
	print(json_text)
	for user_js in json_text:
		print(user_js)
		user = User.query.filter_by(id = user_js['id']).first()

		if user!=None:					
			try:
				db.session.delete(user)	
				db.session.commit()			
			except Exception as ex:
				error = "user: {0} произошла ошибка удаления: {1} ".format(
					user_js['id'], ex)
				return Response(error, status = 500)	
		else:
			error =  "user_id: {0}  - Такого пользователя нет".format(user_js['id'])
			return Response(error, status = 400)	

	return all_user()					



@app.route('/api/user', methods = ['POST'])
@login_required
@csrf.exempt
def insert_user():
	json_text = json.loads(request.json['data'])
	print(json_text)
	for user_js in json_text:
		print(user_js)
		try:
			user = User(username = user_js['username'], name = user_js['name'])
			user.set_password(user_js['password'])	
			db.session.add(user)		
			db.session.commit()
			
		except Exception as ex:
			return "user: {0} произошла ошибка вставки: {1}".format(
					user_js, str(ex))

	return all_user()	


def load_json():

	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	insert_json_url = os.path.join(SITE_ROOT, "static/test_json", "insert.json")
	insert_string = open(insert_json_url)	

	'''возможно, это кастыль, но не нашел другого способа обойти такую ситуацию:
	если в файле каждый новый словарь будет с новой строки, то на странице формы
	js не сможет обработать многостроковый текст:
	[  здесь потребуется "\"
		{a},  и здесь "\"
		{b}, "\"
	]'''

	insert_data = json.load(insert_string)
	'''поэтому, сначала загружаем из файла json, а затем преобразую в строку'''
	insert_data_js = json.dumps(insert_data)
	
	delete_data_js = json.dumps(
		json.load(
			open(
				os.path.join(SITE_ROOT, "static/test_json", "delete.json")
				)
			)
		)

	update_data_js = json.dumps(
		json.load(
			open(
				os.path.join(SITE_ROOT, "static/test_json", "update.json")
				)
			)
		)

	return insert_data_js, delete_data_js, update_data_js

	
