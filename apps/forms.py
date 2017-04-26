from flask_wtf import Form
from wtforms import StringField, BooleanField,PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms import validators



class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired()])

class SignupForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Nickname', validators=[DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class EditProfileForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])