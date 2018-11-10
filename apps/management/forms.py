
from flask_wtf import FlaskForm
from wtforms.validators import  Email,Length,InputRequired,EqualTo
from wtforms import StringField,PasswordField,SubmitField,IntegerField,Form

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(message='Please input email'),Email(message='Please input right format of email')])
    password = StringField(validators=[Length(6,20,message='Please input password with length 6-20')])
    remember = IntegerField()


class Resetpwdform(Form):
    oldpwd = StringField(validators=[Length(6, 20, message='Please input password with length 6-20')])
    newpwd = StringField(validators=[Length(6, 20, message='Please input password with length 6-20')])
    newpwd2 = StringField(validators=[Length(6, 20, message='Please input password with length 6-20'),EqualTo('newpwd')])

    def get_error(self):
        msg = self.errors.popitem()[1][0]
        return msg