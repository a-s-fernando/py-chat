from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired


class userForm(FlaskForm):
    # these validators cause an error of either is unfilled, as we don't want empty tasks in our db
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class messageForm(FlaskForm):
    message = TextAreaField('message', validators=[DataRequired()])


class requestForm(FlaskForm):
    user = StringField('name', validators=[DataRequired()])
