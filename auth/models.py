from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from config import db


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	name = db.Column(db.String(30))
	password_hash = db.Column(db.String(256))

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		a = check_password_hash(self.password_hash, password)
		print(a)
		return a
