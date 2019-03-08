from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired

class InsertForm(FlaskForm):
	command_type = SelectField('Type', choices = [		
		('POST', 'POST'),
		('PUT', 'PUT'),
		('DELETE', 'DELETE')], 
		render_kw ={'class': 'form-control' })
	text = TextAreaField(u'Mailing Address', [validators.optional(), validators.length(max=2000)], 
		render_kw ={'class': 'form-control' })
	
