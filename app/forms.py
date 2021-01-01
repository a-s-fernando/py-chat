from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

class userForm(Form):
	username = TextField('username', validators=[DataRequired()]) #these validators cause an error of either is unfilled, as we don't want empty tasks in our db
	password = TextField('password', validators=[DataRequired()])

class messageForm(Form):
	message = TextAreaField('message', validators=[DataRequired()])

class requestForm(Form):
	user = TextField('name', validators=[DataRequired()])
