from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
from models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[validators.Length(min=4, max=25,
		message = 'Длина логина должна быть больше 4 и меньше 25')], 
		render_kw ={'class': 'form-control' })

	password = PasswordField('Password', validators=[validators.Length(min=4, max=25,
		message = 'Длина пароля должна быть больше 4 и меньше 25')], 
		render_kw ={'class': 'form-control' })    

	submit = SubmitField('Sign In', 
		render_kw ={'class': 'form-control' })


	def check_user_exists(self, user) -> bool:
		'''проверяет, существует есть ли такой User в БД
		если есть, то возвращает True, 
		если нет, то False и добавит ошибку в форму'''
		
		
		if user is None:
			self.username.errors.append('Такой пользователь не зарегистрирован!')			
			return False
		else:
			return True		

	def check_password(self, user) -> bool:

		if user.check_password(password = self.password.data):
			return True
		else:
			self.password.errors.append('Не правильный пароль!')	




	def check(self, user) ->bool:		

		if self.check_user_exists(user) == False:
			return False

		else:
			if self.check_password(user) == False:
				return False

		return True
		
					

class SignUpForm(LoginForm):


	password2 = PasswordField('Password2', validators=[
		DataRequired(),
		validators.EqualTo('password', message = 'Пароли не совпадают')], 
		render_kw ={'class': 'form-control' })

	def check_user_exists(self) -> bool:
		'''Возвращает True, если такой пользователь уже есть в БД,
		Иначе возвращает False'''

		user = User.query.filter_by(username = self.username.data).first()
		if user is not None:
			self.username.errors.append('Такой пользователь уже существует')
			return True
		else:
			return False	