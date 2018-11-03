
from flask_wtf import FlaskForm
from wtforms.validators import  Email,Length,InputRequired
from wtforms import StringField,PasswordField,SubmitField,IntegerField


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(message='Please input email'),Email(message='Please input right format of email')])
    password = StringField(validators=[Length(6,20,message='Please input password with length 6-20')])
    remember = IntegerField()