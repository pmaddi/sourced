from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, TextAreaField


class LoginForm(Form):
    email = TextField('email', validators = [validators.Required()])
    password = PasswordField('password', validators = [validators.Required()])

    
class RegistrationForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=6, max=35)
    ])

class EditForm(Form):
    name = TextField('name', validators = [validators.Required()])
    about_me = TextAreaField('about_me', validators = [validators.Length(min = 0, max = 140)])

class PostForm(Form):
    post = TextField('post', validators = [validators.Required()])